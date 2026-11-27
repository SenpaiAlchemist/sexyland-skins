import re, subprocess, numpy as np
from scipy.signal import fftconvolve
from sf2 import SF2, Renderer

SR = 44100
SF = SF2('/usr/share/sounds/sf2/TimGM6mb.sf2')
R = Renderer(SF, SR)
_cache = {}

NOTE = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}


def midi(n):
    m = re.fullmatch(r'([A-G])(#|b)?(-?\d)', n)
    if not m: raise ValueError(n)
    v = NOTE[m.group(1)] + (1 if m.group(2) == '#' else -1 if m.group(2) == 'b' else 0)
    return 12 * (int(m.group(3)) + 1) + v


def parse(s, default=1.0):
    """'G4:1.5 [C4,E4,G4]:2 r:1 A4' -> list of (beat_offset, [midis], dur). Bare token = default dur.
    'x3( ... )' not supported; repeat by python."""
    out = []; t = 0.0
    for tok in s.split():
        if ':' in tok:
            a, d = tok.rsplit(':', 1); d = float(d)
        else:
            a, d = tok, default
        if a == 'r':
            t += d; continue
        if a.startswith('['):
            ns = [midi(x) for x in a[1:-1].split(',')]
        else:
            ns = [midi(a)]
        out.append((t, ns, d)); t += d
    return out, t


def tnote(bank, prog, key, vel, dur, rel=1.0):
    k = (bank, prog, key, vel, round(dur, 3), rel)
    if k not in _cache:
        _cache[k] = R.note(bank, prog, key, vel, dur, rel)
    return _cache[k]


class Song:
    def __init__(self, bpm):
        self.bpm = bpm; self.events = []  # (sec, bank, prog, key, vel, dursec, gain, pan, rel)

    def spb(self): return 60.0 / self.bpm

    def add(self, prog, seq, at=0.0, vel=90, gain=1.0, legato=1.0, bank=0, pan=0.0, rel=1.0, swing=0.0, human=0.01, default=1.0, transpose=0):
        notes, length = parse(seq, default) if isinstance(seq, str) else seq
        rs = np.random.RandomState(abs(hash((prog, at, seq if isinstance(seq, str) else 0))) % 2**31)
        for (b, ns, d) in notes:
            for k in ns:
                jitter = rs.uniform(-human, human)
                v = int(np.clip(vel + rs.randint(-6, 7), 1, 127))
                self.events.append(((at + b) * self.spb() + max(0, jitter), bank, prog, k + transpose, v, d * self.spb() * legato, gain, pan, rel))
        return at + length

    def drum(self, pattern, at, bars, beats_per_bar=4, kit=0, vel=100, gain=1.0):
        """pattern: dict key->string of chars per step (x=hit, o=accent, .=rest); steps per bar = len."""
        for key, pat in pattern.items():
            steps = len(pat); step = beats_per_bar / steps
            for bar in range(bars):
                for i, c in enumerate(pat):
                    if c in 'xo':
                        v = vel if c == 'o' else int(vel * 0.7)
                        self.events.append((((at + bar * beats_per_bar) + i * step) * self.spb(), 128, kit, key, v, 0.4, gain, 0.0, 1.0))
        return at + bars * beats_per_bar

    def render(self, tail=4.0):
        end = max(e[0] + e[5] for e in self.events) + tail
        buf = np.zeros((int(end * SR) + SR * 4, 2), np.float32)
        for (t, bank, prog, key, vel, dur, gain, pan, rel) in self.events:
            w = tnote(bank, prog, key, vel, dur, rel)
            if w is None: continue
            i = int(t * SR)
            w = w * gain
            if pan:
                w = w * np.array([np.sqrt(0.5 - pan / 2) * 1.414, np.sqrt(0.5 + pan / 2) * 1.414], np.float32)
            buf[i:i + len(w)] += w[:len(buf) - i]
        return buf[:int(end * SR)]


def reverb(x, seconds=2.5, wet=0.3, predelay=0.02, seed=1):
    n = int(seconds * SR)
    rs = np.random.RandomState(seed)
    t = np.arange(n) / SR
    env = np.exp(-t * 6.9 / seconds)
    irL = rs.randn(n) * env; irR = rs.randn(n) * env
    # darken: simple lowpass by cumulative moving average
    k = 6
    irL = np.convolve(irL, np.ones(k) / k, 'same'); irR = np.convolve(irR, np.ones(k) / k, 'same')
    pd = int(predelay * SR)
    irL = np.concatenate([np.zeros(pd), irL]); irR = np.concatenate([np.zeros(pd), irR])
    irL /= np.sqrt((irL ** 2).sum()); irR /= np.sqrt((irR ** 2).sum())
    yL = fftconvolve(x[:, 0], irL)[:len(x)]; yR = fftconvolve(x[:, 1], irR)[:len(x)]
    y = np.stack([yL, yR], 1).astype(np.float32)
    return x * (1 - wet) + y * wet * 1.2


def master(x, fade_in=1.5, fade_out=4.0, peak=0.89, rms_target=0.12):
    x = x.copy()
    rms = np.sqrt((x ** 2).mean()) + 1e-9
    x *= rms_target / rms
    # soft limiter
    x = np.tanh(x * 1.1) / 1.1
    p = np.abs(x).max()
    if p > peak: x *= peak / p
    fi = int(fade_in * SR); fo = int(fade_out * SR)
    x[:fi] *= np.linspace(0, 1, fi)[:, None]
    x[-fo:] *= np.linspace(1, 0, fo)[:, None]
    return x


def save_ogg(x, path, q=3):
    pcm = (np.clip(x, -1, 1) * 32767).astype('<i2').tobytes()
    p = subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 's16le', '-ar', str(SR), '-ac', '2', '-i', '-',
                        '-c:a', 'libvorbis', '-q:a', str(q), path], input=pcm)
    assert p.returncode == 0


def save_mono_ogg(x, path, q=3):
    m = x.mean(1, keepdims=True)
    pcm = (np.clip(m, -1, 1) * 32767).astype('<i2').tobytes()
    p = subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 's16le', '-ar', str(SR), '-ac', '1', '-i', '-',
                        '-c:a', 'libvorbis', '-q:a', str(q), path], input=pcm)
    assert p.returncode == 0
