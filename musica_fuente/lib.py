import numpy as np
from engine import *
from theory import *

# GM programs
PIANO, HARPSI, CELESTA, GLOCK, MUSICBOX, VIBES, MARIMBA, BELLS, DULCIMER = 0, 6, 8, 9, 10, 11, 12, 14, 15
ORGAN, REEDORG, ACCORD = 19, 20, 21
NYLON, STEEL = 24, 25
ABASS, CBASS = 32, 43
VIOLIN, VIOLA, CELLO, TREM, PIZZ, HARP, TIMP = 40, 41, 42, 44, 45, 46, 47
STRINGS, SLOWSTR, CHOIR, OOHS, ORCHHIT = 48, 49, 52, 53, 55
TRUMPET, TROMBONE, TUBA, HORN, BRASS = 56, 57, 58, 60, 61
OBOE, ENGHORN, BASSOON, CLARINET, PICCOLO, FLUTE, RECORDER, PANFLUTE, SHAKU, WHISTLE, OCARINA = 68, 69, 70, 71, 72, 73, 74, 75, 77, 78, 79
PADWARM, PADHALO, PADSWEEP, ATMOS, SOUNDTRACK, BOWEDGLASS = 89, 94, 95, 99, 97, 92
SITAR, BANJO, KOTO, KALIMBA, BAGPIPE, FIDDLE, SHENAI = 104, 105, 107, 108, 109, 110, 111
TAIKO, TOM, SYNDRUM, REVCYM = 116, 117, 118, 119
# GM drum keys
KICK, SNARE, HHC, HHO, CRASH, RIDE, TOML, TOMM, TOMH, TAMB, CLAP = 36, 38, 42, 46, 49, 51, 41, 45, 48, 54, 39


def concat(parts, overlap_tail=True):
    """parts: list of (audio, nominal_len_seconds). Each next part starts at the nominal end of the previous."""
    total = sum(l for _, l in parts) + max(len(a) / SR - l for a, l in parts) + 1
    out = np.zeros((int(total * SR), 2), np.float32)
    t = 0.0
    for a, l in parts:
        i = int(t * SR)
        out[i:i + len(a)] += a[:len(out) - i]
        t += l
    # trim trailing silence
    nz = np.where(np.abs(out).max(1) > 1e-4)[0]
    return out[:nz[-1] + SR // 2] if len(nz) else out


def sec(song, beats):
    return song.render(tail=4.0), beats * song.spb()


def finish(x, path, rv=2.5, wet=0.28, mono=False, fade_out=4.0, rms=0.12, q=3):
    y = master(reverb(x, rv, wet), fade_out=fade_out, rms_target=rms)
    (save_mono_ogg if mono else save_ogg)(y, path, q)
    return len(y) / SR
