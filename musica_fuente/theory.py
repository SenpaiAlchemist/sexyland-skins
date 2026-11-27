import re
from engine import midi

Q = {'': [0, 4, 7], 'm': [0, 3, 7], '7': [0, 4, 7, 10], 'm7': [0, 3, 7, 10], 'maj7': [0, 4, 7, 11],
     'dim': [0, 3, 6], 'aug': [0, 4, 8], 'sus4': [0, 5, 7], 'sus2': [0, 2, 7], '5': [0, 7], 'm6': [0, 3, 7, 9],
     'dim7': [0, 3, 6, 9], 'add9': [0, 4, 7, 14], 'madd9': [0, 3, 7, 14]}
NAMES = ['C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B']


def nm(m):
    return NAMES[m % 12] + str(m // 12 - 1)


def chord(name, octave=3):
    m = re.fullmatch(r'([A-G](?:#|b)?)(.*?)(?:/([A-G](?:#|b)?))?', name)
    root, q, bass = m.group(1), m.group(2), m.group(3)
    r = midi(root + str(octave))
    ns = [r + i for i in Q[q]]
    if bass:
        b = midi(bass + str(octave - 1))
        while b > r - 1: b -= 12
        ns = [b] + ns
    return ns


def tok(ns, d):
    if len(ns) == 1: return f'{nm(ns[0])}:{d}'
    return '[' + ','.join(nm(n) for n in ns) + f']:{d}'


def block(chords, d, octave=3):
    return ' '.join(tok(chord(c, octave), d) for c in chords)


def bass(chords, d, octave=2, pattern=None):
    out = []
    for c in chords:
        ns = chord(c, octave)
        root = ns[0]
        if pattern is None:
            out.append(tok([root], d))
        else:  # pattern of (interval_index_or_'o', dur)
            for p, pd in pattern:
                if p == 'r': out.append(f'r:{pd}')
                elif p == 'o': out.append(tok([root + 12], pd))
                elif p == '5': out.append(tok([root + 7], pd))
                else: out.append(tok([root], pd))
    return ' '.join(out)


def arp(chords, idxs, step, octave=3, span=None):
    """idxs: indices into chord tones extended upwards by octaves, e.g. [0,1,2,3,2,1]."""
    out = []
    for c in chords:
        ns = chord(c, octave)
        ext = ns + [n + 12 for n in ns] + [n + 24 for n in ns]
        for i in idxs:
            out.append('r:%s' % step if i is None else tok([ext[i]], step))
    return ' '.join(out)


def rep(s, n):
    return ' '.join([s] * n)
