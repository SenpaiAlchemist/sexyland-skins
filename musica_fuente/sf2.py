"""Minimal SoundFont2 sample renderer (numpy)."""
import struct, numpy as np

GEN = dict(startAddrsOffset=0, endAddrsOffset=1, startloopAddrsOffset=2, endloopAddrsOffset=3,
           startAddrsCoarseOffset=4, pan=17, attackVolEnv=34, holdVolEnv=35, decayVolEnv=36,
           sustainVolEnv=37, releaseVolEnv=38, instrument=41, keyRange=43, velRange=44,
           endloopAddrsCoarseOffset=45, initialAttenuation=48, coarseTune=51, fineTune=52,
           sampleID=53, sampleModes=54, scaleTuning=56, overridingRootKey=58,
           startloopAddrsCoarseOffset=50, endAddrsCoarseOffset=12)


class SF2:
    def __init__(self, path):
        d = open(path, 'rb').read()
        self.chunks = {}
        self._walk(d, 12, len(d))
        self.smpl = np.frombuffer(self.chunks['smpl'], dtype='<i2').astype(np.float32) / 32768.0
        self.phdr = [struct.unpack('<20sHHHIII', self.chunks['phdr'][i:i+38]) for i in range(0, len(self.chunks['phdr']), 38)]
        self.pbag = [struct.unpack('<HH', self.chunks['pbag'][i:i+4]) for i in range(0, len(self.chunks['pbag']), 4)]
        self.pgen = [struct.unpack('<HH', self.chunks['pgen'][i:i+4]) for i in range(0, len(self.chunks['pgen']), 4)]
        self.inst = [struct.unpack('<20sH', self.chunks['inst'][i:i+22]) for i in range(0, len(self.chunks['inst']), 22)]
        self.ibag = [struct.unpack('<HH', self.chunks['ibag'][i:i+4]) for i in range(0, len(self.chunks['ibag']), 4)]
        self.igen = [struct.unpack('<HH', self.chunks['igen'][i:i+4]) for i in range(0, len(self.chunks['igen']), 4)]
        self.shdr = [struct.unpack('<20sIIIIIBbHH', self.chunks['shdr'][i:i+46]) for i in range(0, len(self.chunks['shdr']), 46)]
        self.cache = {}

    def _walk(self, d, a, b):
        while a < b - 8:
            cid = d[a:a+4].decode('latin1'); ln = struct.unpack('<I', d[a+4:a+8])[0]
            if cid == 'LIST':
                self._walk(d, a + 12, a + 8 + ln)
            else:
                self.chunks[cid] = d[a+8:a+8+ln]
            a += 8 + ln + (ln & 1)

    def presets(self):
        return [(p[2], p[1], p[0].split(b'\0')[0].decode('latin1')) for p in self.phdr[:-1]]

    @staticmethod
    def _zones(bags, gens, i0, i1):
        zs = []
        for bi in range(i0, i1):
            g0, g1 = bags[bi][0], bags[bi+1][0]
            z = {}
            for gi in range(g0, g1):
                op, amt = gens[gi]
                z[op] = amt
            zs.append(z)
        return zs

    def regions(self, bank, prog):
        key = (bank, prog)
        if key in self.cache: return self.cache[key]
        pi = [i for i, p in enumerate(self.phdr[:-1]) if p[2] == bank and p[1] == prog]
        if not pi:
            pi = [i for i, p in enumerate(self.phdr[:-1]) if p[2] == 0 and p[1] == prog]
        pi = pi[0]
        pz = self._zones(self.pbag, self.pgen, self.phdr[pi][3], self.phdr[pi+1][3])
        pglob = pz[0] if pz and 41 not in pz[0] else {}
        regs = []
        for z in pz:
            if 41 not in z: continue
            ii = z[41]
            iz = self._zones(self.ibag, self.igen, self.inst[ii][1], self.inst[ii+1][1])
            iglob = iz[0] if iz and 53 not in iz[0] else {}
            for q in iz:
                if 53 not in q: continue
                g = dict(iglob); g.update(q)
                # preset-level additive gens
                padd = dict(pglob); padd.update(z)
                regs.append((g, padd))
        self.cache[key] = regs
        return regs


def rng(v):
    return v & 0xff, (v >> 8) & 0xff


def s16(v):
    return v - 65536 if v >= 32768 else v


def tc2s(v):  # timecents to seconds
    return 2 ** (s16(v) / 1200.0)


class Renderer:
    def __init__(self, sf, sr=44100):
        self.sf, self.sr = sf, sr

    def note(self, bank, prog, key, vel, dur, rel_scale=1.0):
        out = None
        for g, p in self.sf.regions(bank, prog):
            kl, kh = rng(g.get(43, p.get(43, 0x7f00)))
            vl, vh = rng(g.get(44, p.get(44, 0x7f00)))
            pk = rng(p.get(43, 0x7f00)); pv = rng(p.get(44, 0x7f00))
            if not (kl <= key <= kh and vl <= vel <= vh and pk[0] <= key <= pk[1] and pv[0] <= vel <= pv[1]):
                continue
            sh = self.sf.shdr[g[53]]
            _, start, end, ls, le, rate, okey, corr, _, stype = sh
            start += s16(g.get(0, 0)) + 32768 * s16(g.get(4, 0))
            end += s16(g.get(1, 0)) + 32768 * s16(g.get(12, 0))
            ls += s16(g.get(2, 0)) + 32768 * s16(g.get(50, 0))
            le += s16(g.get(3, 0)) + 32768 * s16(g.get(45, 0))
            root = g.get(58, 0xffff)
            if root == 0xffff or root > 127: root = okey
            tune = s16(g.get(51, 0)) + s16(p.get(51, 0)) + (s16(g.get(52, 0)) + s16(p.get(52, 0)) + corr) / 100.0
            scale = g.get(56, 100) / 100.0
            semis = (key - root) * scale + tune
            ratio = 2 ** (semis / 12.0) * rate / self.sr
            mode = g.get(54, 0) & 3
            att = s16(g.get(48, 0)) / 10.0 + s16(p.get(48, 0)) / 10.0
            A = tc2s(g.get(34, 0xf448)) if 34 in g else 0.001
            Dc = tc2s(g.get(36, 0xf448)) if 36 in g else 0.001
            S = s16(g.get(37, 0)) / 10.0
            R = (tc2s(g.get(38, 0xf448)) if 38 in g else 0.01) * rel_scale
            R = min(max(R, 0.03), 3.0)
            pan = s16(g.get(17, 0)) / 500.0
            n = int((dur + R) * self.sr)
            pos = np.arange(n) * ratio
            data = self.sf.smpl
            if mode in (1, 3) and le > ls + 4:
                L = le - ls
                body = ls - start
                idx = np.where(pos < body + L, pos, body + (pos - body) % L)
                idx = np.where(pos < body, pos, idx)
                src = start + idx
            else:
                src = start + pos
                src = src[src < end - 1]
            i0 = src.astype(np.int64); fr = (src - i0).astype(np.float32)
            i0 = np.clip(i0, 0, len(data) - 2)
            w = data[i0] * (1 - fr) + data[i0 + 1] * fr
            m = len(w)
            t = np.arange(m) / self.sr
            env = np.ones(m, np.float32)
            a = t < A
            env[a] = t[a] / A
            sl = 10 ** (-S / 20.0)
            dmask = (t >= A) & (t < A + Dc)
            env[dmask] = 1 - (1 - sl) * (t[dmask] - A) / Dc
            env[t >= A + Dc] = sl
            if mode == 0 and stype != 0:
                pass
            rmask = t >= dur
            if rmask.any():
                lvl = env[np.argmax(rmask)]
                env[rmask] = lvl * np.exp(-(t[rmask] - dur) * 6.9 / R)
            w = w * env * (10 ** (-att / 20.0)) * (vel / 127.0) ** 1.6
            lp = np.sqrt(np.clip(0.5 - pan, 0, 1)); rp = np.sqrt(np.clip(0.5 + pan, 0, 1))
            st = np.stack([w * lp, w * rp], 1)
            if out is None or len(st) > len(out):
                o2 = np.zeros((len(st), 2), np.float32)
                if out is not None: o2[:len(out)] += out
                out = o2
            out[:len(st)] += st
        return out
