from lib import *
OUT = 'out/'


def danza_hungara():
    # Brahms, Danza Hungara n.5 (arreglo propio, sol menor). 2/4, negra = pulso.
    A = ("G5:1.5 G5:0.25 A5:0.25 Bb5:0.5 A5:0.5 G5:0.5 F#5:0.5 G5:1.5 D5:0.5 "
         "G5:1.5 G5:0.25 A5:0.25 Bb5:0.5 A5:0.5 G5:0.5 F#5:0.5 G5:1.5 Bb5:0.5 "
         "C6:1.5 C6:0.25 D6:0.25 Eb6:0.5 D6:0.5 C6:0.5 Bb5:0.5 A5:0.5 Bb5:0.5 A5:0.5 G5:0.5 F#5:1.5 D5:0.5 "
         "G5:1 A5:0.5 Bb5:0.5 C6:1 Bb5:0.5 A5:0.5 Bb5:0.5 A5:0.5 G5:0.5 F#5:0.5 G5:1.5 r:0.5")
    chA = ['Gm', 'D7', 'Gm', 'Gm', 'D7', 'Gm', 'Cm', 'Cm', 'D', 'D7', 'Gm', 'Cm', 'D7', 'Gm']
    B = ("B5:0.25 A5:0.25 G5:0.25 A5:0.25 B5:0.5 D6:0.5 C6:0.25 B5:0.25 A5:0.25 B5:0.25 C6:0.5 E6:0.5 "
         "D6:0.5 B5:0.5 G5:0.5 B5:0.5 A5:1 D5:1 "
         "B5:0.25 A5:0.25 G5:0.25 A5:0.25 B5:0.5 D6:0.5 C6:0.25 B5:0.25 A5:0.25 B5:0.25 C6:0.5 E6:0.5 "
         "D6:0.5 B5:0.5 A5:0.5 F#5:0.5 G5:1 r:1")
    chB = ['G', 'C', 'G', 'D', 'G', 'C', 'D7', 'G']
    parts = []

    def secA(bpm, lead, double=None, loud=90):
        s = Song(bpm)
        s.add(VIOLIN if lead == 'vn' else lead, A, at=0, vel=loud, gain=1.2, legato=0.95)
        if double: s.add(double, A, at=0, vel=loud - 15, gain=0.6, transpose=-12)
        # acompanamiento: bajo en tiempo 1, acorde en el 2 (estilo csardas)
        s.add(CELLO, bass(chA, 2, 2, [('1', 1), ('r', 1)]), at=0, vel=85, gain=0.9)
        s.add(PIZZ, ' '.join('r:1 ' + tok(chord(c, 4), 0.5) + ' ' + tok(chord(c, 4), 0.5) for c in chA), at=0, vel=80, gain=0.7)
        s.add(STRINGS, block(chA, 2, 3), at=0, vel=55, gain=0.35)
        return sec(s, 28)

    def secB(bpm):
        s = Song(bpm)
        s.add(VIOLIN, B, at=0, vel=100, gain=1.1)
        s.add(FLUTE, B, at=0, vel=85, gain=0.6, transpose=12)
        s.add(CBASS, bass(chB, 2, 2, [('1', 0.5), ('r', 0.5), ('5', 0.5), ('r', 0.5)]), at=0, vel=95, gain=0.9)
        s.add(PIZZ, ' '.join(('r:0.5 ' + tok(chord(c, 4), 0.5) + ' ') * 2 for c in chB), at=0, vel=85, gain=0.7)
        s.add(TIMP, 'G2:0.5 r:3.5 D2:0.5 r:3.5 G2:0.5 r:3.5 D2:0.5 r:1.5 G2:1 r:1', at=0, vel=100, gain=0.7)
        return sec(s, 16)

    s0 = Song(96); s0.add(VIOLIN, 'D5:1', vel=90, gain=1.2); s0.add(CELLO, 'D3:1', vel=70)
    parts.append(sec(s0, 1))
    parts += [secA(100, 'vn'), secA(104, 'vn', VIOLA, 95), secB(150), secB(158), secA(100, FLUTE, VIOLIN, 92), secA(108, 'vn', CELLO, 100)]
    s = Song(80); s.add(STRINGS, '[G2,D3,G3,Bb3,D4,G4]:3', vel=100, gain=1.0); s.add(TIMP, 'G2:0.25 G2:0.25 G2:0.25 G2:0.25 G2:2', vel=110, gain=0.8)
    parts.append(sec(s, 3))
    return finish(concat(parts), OUT + 'castillo/danza_hungara_5.ogg', 2.6, 0.3)


def eine_kleine():
    # Mozart, Pequena serenata nocturna K.525 (I, inicio; arreglo propio)
    o = ("G4:1 r:0.5 D4:0.5 G4:1 r:0.5 D4:0.5 G4:0.5 D4:0.5 G4:0.5 B4:0.5 D5:1 r:1 "
         "C5:1 r:0.5 A4:0.5 C5:1 r:0.5 A4:0.5 C5:0.5 A4:0.5 F#4:0.5 A4:0.5 D4:1 r:1")
    m = ("G4:1.5 B4:0.25 A4:0.25 G4:1 F#4:1 F#4:1.5 A4:0.25 C5:0.25 F#4:1 G4:1 "
         "G4:1.5 B4:0.25 A4:0.25 G4:1 F#4:1 F#4:1.5 A4:0.25 C5:0.25 F#4:1 G4:1 "
         "G4:0.25 F#4:0.25 G4:0.25 A4:0.25 B4:0.25 C5:0.25 D5:0.25 E5:0.25 F#5:0.5 G5:0.5 D5:1 "
         "E5:0.5 C5:0.5 A4:0.5 F#4:0.5 G4:1 r:1")
    chm = ['G', 'D7', 'G', 'D7', 'G', 'D7', 'G', 'D7', 'G', 'D', 'C', 'G']
    parts = []
    for rnd in range(3):
        s = Song(128)
        s.add(VIOLIN, o, vel=100, gain=1.1, legato=0.8)
        s.add(VIOLA, o, vel=90, gain=0.7, transpose=-12, legato=0.8)
        s.add(CELLO, o, vel=95, gain=0.8, transpose=-24, legato=0.8)
        t = 16
        s.add(VIOLIN if rnd != 1 else FLUTE, m, at=t, vel=92, gain=1.0)
        s.add(STRINGS, ' '.join(rep(tok(chord(c, 3), 0.5), 4) for c in chm[:8]) + ' ' + block(chm[8:], 2, 3), at=t, vel=60, gain=0.45, legato=0.7)
        s.add(CELLO, bass(chm[:8], 2, 2, [('1', 0.5), ('r', 0.5), ('1', 0.5), ('r', 0.5), ('5', 0.5), ('r', 0.5), ('1', 0.5), ('r', 0.5)]) + ' ' + bass(chm[8:], 2, 2), at=t, vel=85, gain=0.8)
        if rnd == 2: s.add(HARPSI, m, at=t, vel=70, gain=0.4, transpose=12)
        parts.append(sec(s, t + 24))
    s = Song(100); s.add(STRINGS, '[G2,D3,G3,B3,D4,G4]:4', vel=100); parts.append(sec(s, 4))
    return finish(concat(parts), OUT + 'castillo/serenata_mozart.ogg', 2.4, 0.26)


def minueto():
    # Petzold/Bach, Minueto en sol (BWV Anh. 114)
    A1 = ("D5:1 G4:0.5 A4:0.5 B4:0.5 C5:0.5 D5:1 G4:1 G4:1 E5:1 C5:0.5 D5:0.5 E5:0.5 F#5:0.5 G5:1 G4:1 G4:1 "
          "C5:1 D5:0.5 C5:0.5 B4:0.5 A4:0.5 B4:1 C5:0.5 B4:0.5 A4:0.5 G4:0.5 F#4:1 G4:0.5 A4:0.5 B4:0.5 G4:0.5 A4:3 ")
    A2 = ("D5:1 G4:0.5 A4:0.5 B4:0.5 C5:0.5 D5:1 G4:1 G4:1 E5:1 C5:0.5 D5:0.5 E5:0.5 F#5:0.5 G5:1 G4:1 G4:1 "
          "C5:1 D5:0.5 C5:0.5 B4:0.5 A4:0.5 B4:1 C5:0.5 B4:0.5 A4:0.5 G4:0.5 A4:1 B4:0.5 A4:0.5 G4:0.5 F#4:0.5 G4:3 ")
    B1 = ("B5:1 G5:0.5 A5:0.5 B5:0.5 G5:0.5 A5:1 D5:0.5 E5:0.5 F#5:0.5 D5:0.5 G5:1 E5:0.5 F#5:0.5 G5:0.5 D5:0.5 "
          "C#5:1 B4:0.5 C#5:0.5 A4:1 A4:0.5 B4:0.5 C#5:0.5 D5:0.5 E5:0.5 F#5:0.5 G5:1 F#5:1 E5:1 F#5:1 A4:1 C#5:1 D5:3 ")
    B2 = ("D5:1 G4:0.5 F#4:0.5 G4:1 E5:1 G4:0.5 F#4:0.5 G4:1 D5:1 C5:1 B4:1 A4:0.5 G4:0.5 F#4:0.5 G4:0.5 A4:1 "
          "D4:0.5 E4:0.5 F#4:0.5 G4:0.5 A4:0.5 B4:0.5 C5:1 B4:1 A4:1 B4:0.5 D5:0.5 G4:1 F#4:1 G4:3 ")
    lA1 = ['G', 'G', 'C', 'G', 'C', 'G', 'D', 'D']
    lA2 = ['G', 'G', 'C', 'G', 'C', 'G', 'D7', 'G']
    lB1 = ['G', 'D', 'Em', 'A', 'A', 'Em', 'A7', 'D']
    lB2 = ['G', 'C', 'G', 'D', 'D', 'Am', 'D7', 'G']
    lh = lambda ch: ' '.join(tok([chord(c, 3)[0]], 2) + ' ' + tok(chord(c, 3)[1:], 1) for c in ch)
    s = Song(112)
    t = 0
    for i, inst in enumerate([HARPSI, HARPSI, None]):
        for mel, ch in [(A1, lA1), (A2, lA2), (B1, lB1), (B2, lB2)]:
            if inst is None:
                s.add(FLUTE, mel, at=t, vel=88, gain=0.9)
                s.add(HARP, lh(ch), at=t, vel=75, gain=0.7)
                s.add(STRINGS, block(ch, 3, 3), at=t, vel=50, gain=0.25)
            else:
                s.add(HARPSI, mel, at=t, vel=95, gain=0.9)
                s.add(HARPSI, lh(ch), at=t, vel=80, gain=0.6, transpose=-12)
                if i == 1: s.add(VIOLIN, mel, at=t, vel=70, gain=0.4)
            t += 24
    return finish(concat([sec(s, t)]), OUT + 'castillo/minueto_bach.ogg', 2.0, 0.22)


def canon():
    # Pachelbel, Canon en re (canon real a 3 violines sobre el bajo ostinato)
    bl = 'D3:1 A2:1 B2:1 F#2:1 G2:1 D2:1 G2:1 A2:1'
    ch = ['D', 'A', 'Bm', 'F#m', 'G', 'D', 'G', 'A']
    V = [
        'F#5:1 E5:1 D5:1 C#5:1 B4:1 A4:1 B4:1 C#5:1',
        'D5:1 C#5:1 B4:1 A4:1 G4:1 F#4:1 G4:1 E4:1',
        'D4:0.5 F#4:0.5 A4:0.5 G4:0.5 F#4:0.5 D4:0.5 F#4:0.5 E4:0.5 D4:0.5 B3:0.5 D4:0.5 A4:0.5 G4:0.5 B4:0.5 A4:0.5 G4:0.5',
        'F#4:0.5 D4:0.5 E4:0.5 C#5:0.5 D5:0.5 F#5:0.5 A5:0.5 A4:0.5 B4:0.5 G4:0.5 A4:0.5 F#4:0.5 D4:0.5 D5:0.5 D5:0.75 C#5:0.25',
        'D5:0.25 C#5:0.25 D5:0.25 D4:0.25 C#4:0.25 A4:0.25 E4:0.25 F#4:0.25 D4:0.25 D5:0.25 C#5:0.25 B4:0.25 C#5:0.25 F#5:0.25 A5:0.25 B5:0.25 '
        'G5:0.25 F#5:0.25 E5:0.25 G5:0.25 F#5:0.25 E5:0.25 D5:0.25 C#5:0.25 B4:0.25 A4:0.25 G4:0.25 F#4:0.25 E4:0.25 G4:0.25 F#4:0.25 E4:0.25',
        'D4:0.5 E4:0.5 F#4:0.5 G4:0.5 A4:0.5 E4:0.5 A4:0.5 G4:0.5 F#4:0.5 B4:0.5 A4:0.5 G4:0.5 A4:0.5 G4:0.5 F#4:0.5 E4:0.5',
        'D4:0.5 B3:0.5 B3:0.5 C#4:0.5 D4:0.5 D5:0.5 C#5:0.5 B4:0.5 C#5:0.5 F#5:0.5 A5:0.5 B5:0.5 G5:0.5 F#5:0.5 E5:0.5 G5:0.5',
        'F#5:1.5 F#5:0.5 G5:0.5 F#5:0.5 E5:0.5 D5:0.5 B4:1.5 B4:0.5 C#5:0.5 B4:0.5 A4:0.5 G4:0.5',
        'F#4:2 D5:2 B4:2 C#5:2',
        'A5:0.5 F#5:0.5 G5:0.5 A5:0.5 F#5:0.5 G5:0.5 A5:0.5 A4:0.5 B4:0.5 C#5:0.5 D5:0.5 E5:0.5 F#5:0.5 G5:0.5 F#5:0.5 E5:0.5',
        'F#5:1 E5:1 D5:1 C#5:1 B4:1 A4:1 B4:1 C#5:1',
        'D5:2 A4:2 B4:2 C#5:2',
    ]
    s = Song(60)
    cycles = 16
    for c in range(cycles):
        s.add(CELLO, bl, at=c * 8, vel=80, gain=0.9)
        if c >= 2: s.add(HARP, arp(ch, [0, 1, 2, 4], 0.25, 3), at=c * 8, vel=65, gain=0.5)
        if c >= 6: s.add(STRINGS, block(ch, 1, 3), at=c * 8, vel=45, gain=0.25)
    for vi, (inst, start, pan) in enumerate([(VIOLIN, 1, -0.4), (VIOLIN, 2, 0.4), (VIOLA, 3, 0.0)]):
        for k in range(cycles - start - (1 if vi else 0)):
            s.add(inst, V[k % len(V)], at=(start + k) * 8, vel=88, gain=0.9 if vi < 2 else 0.7, pan=pan, transpose=0 if vi < 2 else 0)
    s.add(STRINGS, '[D2,A2,D3,F#3,A3,D4]:4', at=cycles * 8, vel=80)
    return finish(concat([sec(s, cycles * 8 + 4)]), OUT + 'castillo/canon_pachelbel.ogg', 3.0, 0.32)


def jesu():
    # Bach, Jesus, alegria de los hombres (BWV 147) - tresillos (12/8 como corcheas de tresillo)
    l = ("G4 A4 B4 D5 C5 C5 E5 D5 D5 G5 F#5 G5 D5 B4 G4 A4 B4 C5 D5 E5 D5 C5 B4 A4 "
         "B4 G4 A4 B4 C5 D5 B4 A4 G4 E4 F#4 G4 D4 G4 F#4 G4 A4 B4 C5 B4 A4 G4 F#4 A4 "
         "G4 A4 B4 D5 C5 C5 E5 D5 D5 G5 F#5 G5 D5 B4 G4 A4 B4 C5 D5 E5 D5 C5 B4 A4 "
         "B4 G4 A4 B4 E4 D5 C5 B4 A4 G4 D4 G4 F#4 G4 A4 B4 C5 D5 C5 B4 A4 B4 G4:3")
    step = 1 / 3
    ch = ['G', 'C', 'G', 'G', 'G', 'C', 'G', 'D', 'Em', 'Em', 'G', 'D', 'G', 'C', 'G', 'G', 'Em', 'C', 'G', 'D', 'G', 'D7', 'G', 'G']
    s = Song(72); t = 0
    for rnd, (lead, chor) in enumerate([(STRINGS, None), (ORGAN, CHOIR), (VIOLIN, CHOIR)]):
        notes, ln = parse(l, step)
        s.add(lead, (notes, ln), at=t, vel=85, gain=0.8 if lead == ORGAN else 0.95)
        s.add(CELLO, ' '.join(tok([chord(c, 2)[0]], 1) for c in ch), at=t, vel=80, gain=0.8)
        if chor: s.add(chor, block(ch, 1, 4), at=t, vel=60, gain=0.4)
        if rnd == 0: s.add(HARP, block(ch, 1, 3), at=t, vel=60, gain=0.5)
        t += len(ch)
    s.add(ORGAN, '[G2,D3,G3,B3,D4,G4]:4', at=t, vel=90, gain=0.8)
    return finish(concat([sec(s, t + 4)]), OUT + 'castillo/jesus_alegria_bach.ogg', 3.2, 0.35)


def greensleeves(path=OUT + 'castillo/greensleeves.ogg', mono=False, bardic=False):
    v = ("C5:2 D5:1 E5:1.5 F5:0.5 E5:1 D5:2 B4:1 G4:1.5 A4:0.5 B4:1 C5:2 A4:1 A4:1.5 G#4:0.5 A4:1 B4:2 G#4:1 E4:2 A4:1 "
         "C5:2 D5:1 E5:1.5 F5:0.5 E5:1 D5:2 B4:1 G4:1.5 A4:0.5 B4:1 C5:1.5 B4:0.5 A4:1 G#4:1.5 F#4:0.5 G#4:1 A4:3 A4:2 r:1 ")
    c = ("G5:3 G5:1.5 F#5:0.5 E5:1 D5:2 B4:1 G4:1.5 A4:0.5 B4:1 C5:2 A4:1 A4:1.5 G#4:0.5 A4:1 B4:2 G#4:1 E4:3 "
         "G5:3 G5:1.5 F#5:0.5 E5:1 D5:2 B4:1 G4:1.5 A4:0.5 B4:1 C5:1.5 B4:0.5 A4:1 G#4:1.5 F#4:0.5 G#4:1 A4:3 A4:2 r:1 ")
    chv = ['Am', 'C', 'G', 'Em', 'Am', 'E', 'E', 'Am', 'Am', 'C', 'G', 'Em', 'Am', 'E', 'Am', 'Am']
    chc = ['C', 'C', 'G', 'Em', 'Am', 'E', 'E', 'E', 'C', 'C', 'G', 'Em', 'Am', 'E', 'Am', 'Am']
    s = Song(140)
    s.add(FLUTE if not bardic else RECORDER, 'A4:1', at=0, vel=85)
    t = 1
    leads = [NYLON, FLUTE, VIOLIN, FLUTE] if not bardic else [NYLON, RECORDER, NYLON, FIDDLE]
    for i, lead in enumerate(leads):
        s.add(lead, v + c, at=t, vel=95 if lead == NYLON else 88, gain=1.1 if lead == NYLON else 0.9)
        s.add(NYLON, arp(chv + chc, [0, 2, 4], 1, 3), at=t, vel=68, gain=0.6)
        if not bardic and i >= 1: s.add(STRINGS, block(chv + chc, 3, 3), at=t, vel=48, gain=0.3)
        if not bardic and i >= 2: s.add(CELLO, ' '.join(tok([chord(x, 2)[0]], 3) for x in chv + chc), at=t, vel=70, gain=0.6)
        if bardic and i >= 1: s.add(TOM, rep('C3:1 r:2', 32), at=t, vel=60, gain=0.25)
        t += 96
    s.add(NYLON, '[A2,E3,A3,C4,E4]:3', at=t, vel=90)
    return finish(concat([sec(s, t + 3)]), path, 2.2 if not bardic else 1.4, 0.28 if not bardic else 0.18, mono=mono)


def primavera():
    # Vivaldi, La primavera (I, inicio; arreglo propio)
    m = ("E5:1 G#5:0.5 G#5:0.5 G#5:0.5 F#5:0.25 E5:0.25 B5:1.5 r:0.5 "
         "B5:0.25 A5:0.25 G#5:0.5 G#5:0.5 G#5:0.5 F#5:0.25 E5:0.25 B5:1.5 r:0.5 "
         "B5:0.25 A5:0.25 G#5:0.5 A5:0.5 B5:0.5 A5:1 G#5:0.5 F#5:1 r:0.5 "
         "B4:0.25 A4:0.25 G#4:0.5 A4:0.5 B4:0.5 A4:1 G#4:0.5 F#4:1 r:0.5 ")
    ch = ['E', 'E', 'E', 'E', 'E', 'B7', 'E', 'B7']
    birds = ' '.join(['E6:0.125 F#6:0.125'] * 16 + ['B5:0.125 C#6:0.125'] * 8 + ['G#5:0.125 A5:0.125'] * 8)
    s = Song(104); t = 0
    for r in range(3):
        s.add(VIOLIN, m, at=t, vel=100, gain=1.0)
        s.add(VIOLIN, m, at=t, vel=80, gain=0.5, transpose=-12, pan=0.3)
        s.add(STRINGS, ' '.join(rep(tok(chord(c, 3), 0.5), 4) for c in ch), at=t, vel=60, gain=0.4, legato=0.6)
        s.add(CELLO, ' '.join(rep(tok([chord(c, 2)[0]], 0.5), 4) for c in ch), at=t, vel=80, gain=0.7, legato=0.6)
        t += 16
        s.add(VIOLIN, birds, at=t, vel=75, gain=0.6, pan=-0.4)
        s.add(FLUTE, birds, at=t + 0.5, vel=70, gain=0.4, pan=0.4)
        s.add(STRINGS, '[E3,G#3,B3]:4 [E3,G#3,B3]:4', at=t, vel=45, gain=0.3)
        s.add(HARPSI, arp(['E', 'E', 'A', 'B7'], [0, 1, 2, 3], 0.5, 3), at=t, vel=60, gain=0.4)
        t += 8
    s.add(STRINGS, '[E2,B2,E3,G#3,B3,E4]:4', at=t, vel=100)
    return finish(concat([sec(s, t + 4)]), OUT + 'castillo/primavera_vivaldi.ogg', 2.4, 0.26)


def salon(path=OUT + 'castillo/ambiente_salon.ogg', seed=3):
    # original: ambiente tranquilo del gran salon (re dorico)
    rs = np.random.RandomState(seed)
    ch = ['Dm', 'C', 'G/B', 'Dm', 'Bb', 'F', 'C', 'Dm', 'Gm', 'Dm', 'Bb', 'A', 'Dm', 'C', 'Dm', 'Dm']
    s = Song(66); t = 0
    scale = [62, 64, 65, 67, 69, 71, 72, 74, 76, 77]
    for r in range(3):
        s.add(SLOWSTR, block(ch, 4, 3), at=t, vel=60, gain=0.6)
        s.add(HARP, arp(ch, [0, 1, 2, 3, 4, 3, 2, 1], 0.5, 3), at=t, vel=60, gain=0.55)
        s.add(CBASS, ' '.join(tok([chord(c, 2)[0]], 4) for c in ch), at=t, vel=60, gain=0.5)
        if r >= 1:
            mel = []; cur = 4
            for b in range(len(ch) * 2):
                cur = int(np.clip(cur + rs.choice([-2, -1, -1, 0, 1, 1, 2]), 0, len(scale) - 1))
                mel.append(tok([scale[cur]], rs.choice([1, 2, 2, 3]) if b % 2 else 2))
            mm = parse(' '.join(mel))
            s.add(FLUTE if r == 1 else OBOE, mm, at=t, vel=70, gain=0.55)
        t += len(ch) * 4
    return finish(concat([sec(s, t)]), path, 3.5, 0.4, rms=0.09)


ALL = [danza_hungara, eine_kleine, minueto, canon, jesu, greensleeves, primavera, salon]
