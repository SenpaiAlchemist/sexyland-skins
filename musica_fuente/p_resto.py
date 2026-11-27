from lib import *
import p_castillo
OUT = 'out/'


def rand_melody(rs, scale, n, durs, start=None):
    cur = start if start is not None else len(scale) // 2
    out = []
    for _ in range(n):
        cur = int(np.clip(cur + rs.choice([-2, -1, -1, 0, 1, 1, 2, 3, -3]), 0, len(scale) - 1))
        out.append(tok([scale[cur]], rs.choice(durs)))
    return ' '.join(out)


# ---------------- TORRE VALYRIA ----------------
def toccata():
    # Bach, Tocata y fuga en re menor BWV 565 (inicio; arreglo propio)
    s = Song(60)
    t = s.add(ORGAN, 'A5:0.125 G5:0.125 A5:1.75 r:0.5 G5:0.125 F5:0.125 E5:0.125 D5:0.125 C#5:1 D5:2 r:1', at=0, vel=110)
    t = s.add(ORGAN, 'A4:0.125 G4:0.125 A4:1.75 r:0.5 E4:0.25 F4:0.25 C#4:0.5 D4:2 r:1', at=t, vel=110)
    t = s.add(ORGAN, 'A3:0.125 G3:0.125 A3:1.75 r:0.5 G3:0.125 F3:0.125 E3:0.125 D3:0.125 C#3:1 D3:2.5', at=t, vel=110)
    s.add(ORGAN, 'D2:6', at=t - 2.5, vel=100)
    t += 0.5
    roll = 'C#3:0.125 E3:0.125 G3:0.125 Bb3:0.125 C#4:0.125 E4:0.125 G4:0.125 Bb4:0.125'
    t = s.add(ORGAN, roll, at=t, vel=105)
    s.add(ORGAN, '[C#4,E4,G4,Bb4]:2.5', at=t, vel=105); t += 2.5
    s.add(ORGAN, '[D3,F3,A3,D4,F4]:3', at=t, vel=110); s.add(ORGAN, 'D2:3', at=t, vel=110); t += 3.5
    # seccion rapida en semicorcheas (estilo, sobre pedal)
    fig = 'A4:0.25 G4:0.25 F4:0.25 E4:0.25 D4:0.25 C#4:0.25 D4:0.25 A3:0.25 '
    fig2 = 'Bb4:0.25 A4:0.25 G4:0.25 F4:0.25 E4:0.25 D4:0.25 E4:0.25 A3:0.25 '
    fig3 = 'G4:0.25 F4:0.25 E4:0.25 D4:0.25 C#4:0.25 Bb3:0.25 C#4:0.25 A3:0.25 '
    s2 = Song(84); u = 0
    for k in range(3):
        for f, pd in [(fig, 'D2'), (fig2, 'G2'), (fig3, 'A2'), (fig, 'D2')]:
            s2.add(ORGAN, rep(f, 2), at=u, vel=100, gain=0.9, transpose=12 if k == 1 else 0)
            s2.add(ORGAN, f'{pd}:4', at=u, vel=95, gain=0.8)
            u += 4
    s2.add(ORGAN, '[D3,A3,D4,F4,A4,D5]:6', at=u, vel=115); s2.add(ORGAN, 'D2:6', at=u, vel=115); u += 6
    return finish(concat([sec(s, t), sec(s2, u)]), OUT + 'valyria/tocata_bach.ogg', 4.5, 0.42)


def dies_irae():
    chant = 'F3:1 E3:1 F3:1 D3:1 E3:1 C3:1 D3:2 F3:1 F3:1 G3:1 F3:1 E3:1 D3:1 C3:1 E3:1 F3:1 E3:1 D3:2 r:2'
    s = Song(58); t = 0
    for r in range(5):
        s.add(ORGAN, 'D2:12', at=t, vel=80, gain=0.5); s.add(ORGAN, 'A2:12', at=t + 12, vel=80, gain=0.5)
        s.add(CHOIR, chant, at=t, vel=90 + 5 * r, gain=1.0, transpose=12)
        if r >= 1: s.add(CHOIR, chant, at=t, vel=80, gain=0.6)
        if r >= 2: s.add(CELLO, chant, at=t, vel=85, gain=0.6, transpose=-12)
        if r >= 3: s.add(TROMBONE, chant, at=t, vel=80, gain=0.5)
        s.add(TIMP, 'D2:1 r:7 D2:1 r:7 A1:1 r:7', at=t, vel=100, gain=0.6)
        t += 24
    s.add(CHOIR, '[D3,A3,D4,F4]:6', at=t, vel=100); s.add(ORGAN, '[D2,A2,D3]:6', at=t, vel=100)
    return finish(concat([sec(s, t + 6)]), OUT + 'valyria/dies_irae.ogg', 5.0, 0.45, rms=0.11)


def claro_luna():
    # Beethoven, Sonata Claro de luna (I; arreglo propio)
    trip = lambda a, b, c, n=4: f'{a}:{1/3} {b}:{1/3} {c}:{1/3} ' * n
    bars = [
        (trip('G#3', 'C#4', 'E4'), '[C#2,C#3]:4', None),
        (trip('G#3', 'C#4', 'E4'), '[B1,B2]:4', None),
        (trip('A3', 'C#4', 'E4', 2) + trip('A3', 'D4', 'F#4', 2), '[A1,A2]:2 [F#1,F#2]:2', None),
        (trip('G#3', 'B#3', 'F#4', 2) + trip('G#3', 'C#4', 'E4', 2), '[G#1,G#2]:4', None),
        (trip('G#3', 'C#4', 'E4'), '[C#2,C#3]:4', 'r:3 G#4:0.75 G#4:0.25'),
        (trip('A3', 'C#4', 'E4'), '[A1,A2]:4', 'G#4:4'),
        (trip('A3', 'D4', 'F#4'), '[F#1,F#2]:4', 'A4:3 A4:0.75 G#4:0.25'),
        (trip('G#3', 'B#3', 'F#4'), '[G#1,G#2]:4', 'G#4:2 F#4:2'),
        (trip('G#3', 'C#4', 'E4'), '[C#2,C#3]:4', 'E4:2 r:1 G#4:0.75 G#4:0.25'),
        (trip('G#3', 'C#4', 'E4'), '[B1,B2]:4', 'G#4:4'),
        (trip('A3', 'C#4', 'E4'), '[A1,A2]:4', 'A4:3 A4:0.75 G#4:0.25'),
        (trip('G#3', 'B#3', 'F#4'), '[G#1,G#2]:4', 'G#4:2 F#4:2'),
        (trip('G#3', 'C#4', 'E4'), '[C#2,C#3]:4', 'E4:4'),
    ]
    s = Song(54); t = 0
    for r in range(2):
        for rh, lh, mel in bars:
            s.add(PIANO, rh, at=t, vel=62, gain=0.9, rel=2.0)
            s.add(PIANO, lh, at=t, vel=70, gain=0.9, rel=2.0)
            if r == 1: s.add(SLOWSTR, lh, at=t, vel=50, gain=0.35, transpose=12)
            if mel: s.add(PIANO, mel, at=t, vel=85, gain=1.0, rel=2.0)
            if mel and r == 1: s.add(CELLO, mel, at=t, vel=65, gain=0.4, transpose=-12)
            t += 4
    s.add(PIANO, '[C#2,C#3,G#3,C#4,E4]:6', at=t, vel=60, rel=2.0)
    return finish(concat([sec(s, t + 6)]), OUT + 'valyria/claro_de_luna.ogg', 3.0, 0.35, rms=0.1)


def ambiente_dragon(path=OUT + 'valyria/aliento_del_dragon.ogg'):
    rs = np.random.RandomState(7)
    s = Song(70); t = 0
    ch = ['Dm', 'Bb', 'Gm', 'A', 'Dm', 'Eb', 'C', 'A']
    for r in range(4):
        s.add(PADSWEEP, block(ch, 4, 3), at=t, vel=70, gain=0.55)
        s.add(CBASS, ' '.join(tok([chord(c, 1)[0]], 4) for c in ch), at=t, vel=80, gain=0.7)
        s.add(TAIKO, rep('D2:1.5 D2:0.5 r:2', 8), at=t, vel=95 if r else 70, gain=0.7)
        if r >= 1: s.add(HORN, rand_melody(rs, [50, 52, 53, 55, 57, 58, 60, 62], 10, [2, 3, 3, 4]), at=t, vel=80, gain=0.6)
        if r >= 2: s.add(CHOIR, block(ch, 4, 4), at=t, vel=60, gain=0.45)
        if r == 3: s.add(TIMP, rep('D2:0.25 ' * 8 + 'r:2', 8), at=t, vel=85, gain=0.4)
        t += 32
    return finish(concat([sec(s, t)]), path, 4.0, 0.4, rms=0.11)


def cripta(path=OUT + 'valyria/eco_de_la_cripta.ogg'):
    rs = np.random.RandomState(11)
    s = Song(50); t = 0
    for r in range(5):
        s.add(BOWEDGLASS, '[D3,A3]:8 [C3,G3]:8', at=t, vel=70, gain=0.6)
        s.add(ORGAN, 'D2:16', at=t, vel=55, gain=0.35)
        s.add(CELESTA, rand_melody(rs, [62, 63, 65, 67, 68, 70, 72, 74], 12, [1, 1.5, 2]), at=t, vel=55, gain=0.4)
        if r % 2: s.add(BELLS, 'D4:8 A3:8', at=t, vel=60, gain=0.35)
        t += 16
    return finish(concat([sec(s, t)]), path, 6.0, 0.55, rms=0.08)


# ---------------- BARDOS (mono, posicionales) ----------------
def scarborough():
    m = ("D4:2 D4:1 A4:2 A4:1 E4:1.5 F4:0.5 E4:1 D4:3 r:1 A4:1 C5:1 D5:2 C5:1 A4:1 B4:1 G4:1 A4:3 "
         "r:1 r:1 D5:1 D5:2 D5:1 C5:2 A4:1 A4:1 G4:1 F4:1 E4:1 C4:2 D4:2 A4:1 G4:2 F4:1 E4:1 D4:1 C4:1 D4:3 ")
    ch = ['Dm', 'Dm', 'C', 'Dm', 'Dm', 'F', 'G', 'Dm', 'Dm', 'Dm', 'F', 'C', 'C', 'Dm', 'C', 'Dm']
    s = Song(96); t = 0
    for i, lead in enumerate([NYLON, RECORDER, FLUTE, NYLON]):
        s.add(lead, m, at=t, vel=92, gain=1.0 if lead == NYLON else 0.8, transpose=12 if lead == RECORDER else 0)
        s.add(NYLON, arp(ch, [0, 1, 2], 1, 3), at=t, vel=66, gain=0.6)
        if i in (1, 2): s.add(HARP, block(ch, 3, 2), at=t, vel=60, gain=0.4)
        t += 48
    return finish(concat([sec(s, t)]), OUT + 'bardo/scarborough_fair.ogg', 1.5, 0.18, mono=True)


def marinero():
    v = ("A4:0.5 A4:0.25 A4:0.25 A4:0.5 A4:0.25 A4:0.25 A4:0.5 D4:0.5 F4:0.5 A4:0.5 "
         "G4:0.5 G4:0.25 G4:0.25 G4:0.5 G4:0.25 G4:0.25 G4:0.5 C4:0.5 E4:0.5 G4:0.5 "
         "A4:0.5 A4:0.25 A4:0.25 A4:0.5 A4:0.25 A4:0.25 A4:0.5 B4:0.5 C5:0.5 D5:0.5 "
         "C5:0.5 A4:0.5 G4:0.5 E4:0.5 D4:1 D4:1 ")
    c = ("A4:1 A4:1 A4:0.5 D4:0.5 F4:0.5 A4:0.5 G4:1 G4:1 G4:0.5 C4:0.5 E4:0.5 G4:0.5 "
         "A4:1 A4:1 A4:0.5 B4:0.5 C5:0.5 D5:0.5 C5:0.5 A4:0.5 G4:0.5 E4:0.5 D4:1 D4:1 ")
    ch = ['Dm', 'Dm', 'C', 'C', 'Dm', 'Dm', 'C', 'Dm']
    s = Song(130); t = 0
    for i in range(4):
        for mel in (v, c):
            s.add(FIDDLE, mel, at=t, vel=100, gain=1.0)
            if i % 2: s.add(ACCORD, mel, at=t, vel=80, gain=0.5, transpose=-12)
            s.add(ACCORD, ' '.join(('r:0.5 ' + tok(chord(x, 3), 0.5) + ' ') * 2 for x in ch), at=t, vel=75, gain=0.45)
            s.add(ABASS, bass(ch, 2, 2, [('1', 1), ('5', 1)]), at=t, vel=85, gain=0.7)
            s.add(TOM, rep('C3:0.5 r:0.5 G3:0.5 r:0.5', 8), at=t, vel=80, gain=0.4)
            t += 16
    return finish(concat([sec(s, t)]), OUT + 'bardo/marinero_borracho.ogg', 1.2, 0.15, mono=True)


def oda_alegria():
    m = ("E4 E4 F4 G4 G4 F4 E4 D4 C4 C4 D4 E4 E4:1.5 D4:0.5 D4:2 "
         "E4 E4 F4 G4 G4 F4 E4 D4 C4 C4 D4 E4 D4:1.5 C4:0.5 C4:2 "
         "D4 D4 E4 C4 D4 E4:0.5 F4:0.5 E4 C4 D4 E4:0.5 F4:0.5 E4 D4 C4 D4 G3:2 "
         "E4 E4 F4 G4 G4 F4 E4 D4 C4 C4 D4 E4 D4:1.5 C4:0.5 C4:2")
    ch = ['C', 'G', 'C', 'G', 'C', 'G', 'C', 'C', 'G', 'C', 'G', 'C', 'G', 'C', 'G', 'G', 'C', 'G', 'C', 'G', 'C', 'G', 'G', 'C']
    ch = ['C', 'C', 'G', 'G', 'C', 'C', 'G', 'G', 'C', 'C', 'G', 'C', 'G', 'C', 'G', 'G', 'C', 'C', 'G', 'C']
    s = Song(110); t = 0
    for i, lead in enumerate([RECORDER, NYLON, FIDDLE, RECORDER]):
        s.add(lead, m, at=t, vel=92, gain=0.9, transpose=12 if lead == RECORDER else 12)
        s.add(NYLON, arp(ch[:16], [0, 2, 1, 2], 0.5, 3), at=t, vel=64, gain=0.55)
        if i >= 2: s.add(TOM, rep('C3:1 r:1', 16), at=t, vel=60, gain=0.3)
        t += 32
    return finish(concat([sec(s, t)]), OUT + 'bardo/oda_a_la_alegria.ogg', 1.4, 0.16, mono=True)


def jiga(path=OUT + 'bardo/jiga_de_la_taberna.ogg'):
    # original, 6/8 (corcheas = 0.5)
    A = ("D5:0.5 F#5:0.5 A5:0.5 F#5:0.5 D5:0.5 F#5:0.5 G5:0.5 E5:0.5 C#5:0.5 A4:0.5 C#5:0.5 E5:0.5 "
         "D5:0.5 F#5:0.5 A5:0.5 B5:0.5 A5:0.5 F#5:0.5 G5:0.5 E5:0.5 C#5:0.5 D5:1.5 ")
    B = ("A5:0.5 B5:0.5 A5:0.5 G5:0.5 F#5:0.5 E5:0.5 F#5:0.5 G5:0.5 F#5:0.5 E5:0.5 D5:0.5 C#5:0.5 "
         "D5:0.5 E5:0.5 F#5:0.5 G5:0.5 A5:0.5 F#5:0.5 E5:0.5 C#5:0.5 A4:0.5 D5:1.5 ")
    chA = ['D', 'A', 'D', 'A7']; chB = ['D', 'A', 'G', 'A7']
    s = Song(115); t = 0
    for i in range(5):
        for mel, ch in [(A, chA), (A, chA), (B, chB), (B, chB)]:
            s.add(FIDDLE, mel.replace('D5:1.5 ', 'D5:1.5'), at=t, vel=100, gain=1.0)
            if i >= 1: s.add(WHISTLE if i % 2 else ACCORD, mel, at=t, vel=80, gain=0.5, transpose=12 if i % 2 else 0)
            s.add(NYLON, ' '.join(tok(chord(c, 3), 1.5) + ' ' + tok(chord(c, 3), 1.5) for c in ch), at=t, vel=70, gain=0.5, legato=0.6)
            s.add(TOM, rep('C3:1 C3:0.5 G3:1 r:0.5', 4), at=t, vel=75, gain=0.35)
            t += 12
    return finish(concat([sec(s, t)]), path, 1.2, 0.15, mono=True)


def balada(path=OUT + 'bardo/balada_del_viajero.ogg'):
    m = ("A4:1.5 B4:0.5 C5:1 E5:1 D5:2 C5:1 B4:1 A4:1.5 G4:0.5 E4:1 G4:1 A4:4 "
         "C5:1.5 D5:0.5 E5:1 G5:1 F5:2 E5:1 D5:1 C5:1.5 B4:0.5 G4:1 B4:1 A4:4 "
         "E5:1.5 F5:0.5 E5:1 D5:1 C5:2 B4:1 A4:1 G4:1.5 A4:0.5 B4:1 G4:1 E4:4 "
         "A4:1.5 B4:0.5 C5:1 E5:1 D5:1.5 C5:0.5 B4:1 G4:1 A4:4 A4:4 ")
    ch = ['Am', 'F', 'C', 'Am', 'C', 'Dm', 'G', 'Am', 'Am', 'F', 'G', 'Em', 'Am', 'Dm', 'E', 'Am', 'Am']
    s = Song(84); t = 0
    for i, lead in enumerate([NYLON, FLUTE, NYLON]):
        s.add(lead, m, at=t, vel=90, gain=1.0 if lead == NYLON else 0.8)
        s.add(NYLON, arp(ch[:16], [0, 2, 4, 2, 3, 2, 4, 2], 0.5, 3), at=t, vel=62, gain=0.55)
        if i == 1: s.add(CELLO, ' '.join(tok([chord(c, 2)[0]], 4) for c in ch[:16]), at=t, vel=60, gain=0.4)
        t += 64
    return finish(concat([sec(s, t)]), path, 1.6, 0.2, mono=True)


def greensleeves_laud():
    return p_castillo.greensleeves(OUT + 'bardo/greensleeves_laud.ogg', mono=True, bardic=True)


# ---------------- MISIONES ----------------
def mision_inicio():
    s = Song(100)
    s.add(TIMP, ' '.join(['C2:0.125'] * 8), vel=90, gain=0.7)
    s.add(TRUMPET, 'G4:0.5 C5:0.5 E5:0.5 G5:1.5 E5:0.5 G5:2.5', at=1, vel=105)
    s.add(HORN, '[C4,E4]:1.5 [E4,G4]:1.5 [C4,G4]:2.5', at=1, vel=90)
    s.add(STRINGS, '[C3,G3,C4,E4]:3.5', at=2.5, vel=85); s.add(TIMP, 'C2:0.5 r:2.5 G1:1', at=1, vel=100, gain=0.7)
    return finish(concat([sec(s, 7)]), OUT + 'mision/mision_aceptada.ogg', 2.2, 0.3, fade_out=1.5, rms=0.13)


def mision_completada():
    s = Song(116)
    s.add(TRUMPET, 'G4:0.5 G4:0.5 C5:1 E5:0.5 D5:0.5 C5:0.5 D5:0.5 E5:1 G5:1 C6:3', vel=110)
    s.add(HORN, '[E4,G4]:2 [F4,A4]:2 [G4,B4]:2 [E4,G4,C5]:3', vel=95)
    s.add(STRINGS, '[C3,G3,C4]:2 [F3,A3,C4]:2 [G3,B3,D4]:2 [C3,G3,C4,E4]:3', vel=90)
    s.add(TIMP, 'C2:0.5 r:1.5 F1:0.5 r:1.5 G1:0.25 G1:0.25 G1:0.25 G1:0.25 r:1 C2:2', vel=105, gain=0.8)
    s.add(GLOCK, 'C6:0.5 E6:0.5 G6:0.5 C7:1.5', at=6, vel=80, gain=0.5)
    return finish(concat([sec(s, 10)]), OUT + 'mision/mision_completada.ogg', 2.4, 0.3, fade_out=1.5, rms=0.13)


def mision_fallida():
    s = Song(66)
    s.add(OBOE, 'E5:1 D5:1 C5:1 B4:1 A4:2 G#4:1 A4:3', vel=85)
    s.add(SLOWSTR, '[A2,E3,A3,C4]:2 [F2,C3,F3,A3]:2 [E2,B2,E3,G#3]:2 [A2,E3,A3,C4]:4', vel=70)
    s.add(TIMP, 'A1:4 r:2 A1:4', vel=70, gain=0.5)
    return finish(concat([sec(s, 10)]), OUT + 'mision/mision_fallida.ogg', 3.0, 0.35, fade_out=2.5, rms=0.1)


def descubrimiento():
    s = Song(120)
    s.add(CELESTA, 'C6:0.25 E6:0.25 G6:0.25 C7:0.25 E7:1.5', vel=90)
    s.add(HARP, 'C5:0.25 E5:0.25 G5:0.25 C6:0.25 [C5,E5,G5,C6]:1.5', vel=80, gain=0.7)
    s.add(PADHALO, '[C4,E4,G4]:3', vel=60, gain=0.4)
    return finish(concat([sec(s, 4)]), OUT + 'mision/secreto_descubierto.ogg', 2.5, 0.35, fade_out=1.5, rms=0.1)


def misterio():
    rs = np.random.RandomState(5)
    s = Song(56); t = 0
    for r in range(4):
        s.add(PADWARM, '[C3,F#3,Bb3]:8 [D3,G#3,C4]:8', at=t, vel=65, gain=0.5)
        s.add(CELESTA, rand_melody(rs, [60, 62, 64, 66, 68, 70, 72, 74], 10, [1, 1.5, 2]), at=t, vel=60, gain=0.45)
        s.add(PIZZ, rep('C3:1 r:1 F#3:1 r:1', 4), at=t, vel=55, gain=0.4)
        if r >= 1: s.add(CLARINET, rand_melody(rs, [48, 50, 52, 54, 56, 58, 60], 6, [2, 3]), at=t, vel=65, gain=0.4)
        t += 16
    return finish(concat([sec(s, t)]), OUT + 'mision/misterio.ogg', 3.5, 0.4, rms=0.08)


def viaje():
    ch = ['D', 'Bm', 'G', 'A', 'D', 'F#m', 'G', 'A', 'Bm', 'G', 'D', 'A', 'G', 'A', 'D', 'D']
    m = ("A4:2 D5:1 E5:1 F#5:3 E5:1 D5:2 B4:2 C#5:2 A4:2 A4:2 D5:1 E5:1 F#5:2 A5:2 G5:3 F#5:1 E5:4 "
         "F#5:2 E5:1 D5:1 B4:3 D5:1 D5:2 C#5:1 B4:1 A4:4 B4:2 C#5:2 D5:2 E5:2 F#5:4 F#5:4 ")
    s = Song(110); t = 0
    for i in range(3):
        s.add(STRINGS, ' '.join(rep(tok(chord(c, 3), 0.5), 8) for c in ch), at=t, vel=65, gain=0.45, legato=0.55)
        s.add(CELLO, ' '.join(tok([chord(c, 2)[0]], 1) + ' ' + tok([chord(c, 2)[0] + 7], 1) + ' ' + tok([chord(c, 2)[0] + 12], 1) + ' ' + tok([chord(c, 2)[0] + 7], 1) for c in ch), at=t, vel=80, gain=0.7)
        s.add(HORN if i != 1 else FLUTE, m, at=t, vel=90, gain=0.9, transpose=-12 if i != 1 else 0)
        if i == 2: s.add(VIOLIN, m, at=t, vel=85, gain=0.7)
        s.add(TIMP, rep('D2:1 r:3', 16), at=t, vel=75, gain=0.4)
        t += 64
    s.add(STRINGS, '[D2,A2,D3,F#3,A3,D4]:4', at=t, vel=95)
    return finish(concat([sec(s, t + 4)]), OUT + 'mision/viaje_heroico.ogg', 2.5, 0.28)


def triste():
    ch = ['Em', 'C', 'Am', 'B7', 'Em', 'C', 'D', 'B', 'C', 'G', 'Am', 'Em', 'C', 'Am', 'B7', 'Em']
    m = ("B4:3 G4:1 A4:2 E4:2 C5:3 B4:1 A4:2 F#4:2 B4:3 G4:1 E5:2 D5:2 C5:2 B4:2 D#5:4 "
         "E5:3 D5:1 C5:2 B4:2 A4:3 B4:1 G4:4 E5:2 C5:2 A4:2 F#4:2 G4:2 F#4:2 E4:4 ")
    s = Song(60); t = 0
    for i in range(2):
        s.add(PIANO, arp(ch, [0, 1, 2, 3, 2, 1, 2, 1], 0.5, 3), at=t, vel=55, gain=0.7, rel=2)
        s.add(CELLO if i == 0 else VIOLIN, m, at=t, vel=80, gain=0.8, transpose=-12 if i == 0 else 0)
        if i == 1: s.add(SLOWSTR, block(ch, 4, 3), at=t, vel=45, gain=0.3)
        t += 64
    return finish(concat([sec(s, t)]), OUT + 'mision/lamento.ogg', 3.0, 0.35, rms=0.09)


# ---------------- ARENA ----------------
def rey_montana():
    # Grieg, En la gruta del rey de la montana (arreglo propio, acelerando)
    a1 = 'B3:0.5 C#4:0.5 D4:0.5 E4:0.5 F#4:0.5 D4:0.5 F#4:1 F4:0.5 C#4:0.5 F4:1 E4:0.5 C4:0.5 E4:1 '
    a2 = 'B3:0.5 C#4:0.5 D4:0.5 E4:0.5 F#4:0.5 D4:0.5 F#4:0.5 B4:0.5 A4:0.5 F#4:0.5 D4:0.5 F#4:0.5 A4:2 '
    b1 = 'F#4:0.5 G#4:0.5 A#4:0.5 B4:0.5 C#5:0.5 A#4:0.5 C#5:1 D5:0.5 A#4:0.5 D5:1 C#5:0.5 A#4:0.5 C#5:1 '
    b2 = 'F#4:0.5 G#4:0.5 A#4:0.5 B4:0.5 C#5:0.5 A#4:0.5 C#5:0.5 F#5:0.5 E5:0.5 C#5:0.5 A#4:0.5 C#5:0.5 E5:2 '
    parts = []
    plan = [(84, [BASSOON, PIZZ], 0), (100, [BASSOON, CELLO, PIZZ], 0), (118, [STRINGS, CLARINET], 1),
            (138, [STRINGS, HORN, TROMBONE], 2), (160, [STRINGS, BRASS, TRUMPET], 3), (186, [STRINGS, BRASS, TRUMPET, PICCOLO], 3)]
    for bpm, insts, lvl in plan:
        s = Song(bpm)
        for k, ins in enumerate(insts):
            tr = -12 if ins in (BASSOON, CELLO, TROMBONE) else (12 if ins == PICCOLO else 0)
            s.add(ins, a1 + a2 + b1 + b2, vel=80 + lvl * 10, gain=0.8, transpose=tr, legato=0.6)
        s.add(PIZZ if lvl < 2 else CBASS, rep('B1:0.5 r:0.5 F#2:0.5 r:0.5', 4) + ' ' + rep('F#1:0.5 r:0.5 C#2:0.5 r:0.5', 4), vel=85, gain=0.7, legato=0.5)
        if lvl >= 1: s.add(TIMP, rep('B1:1 F#1:1', 8), vel=85 + lvl * 8, gain=0.6)
        if lvl >= 3: s.drum({CRASH: 'x' + '.' * 15, SNARE: '....x.......x...', KICK: 'x.......x.......'}, 0, 2, 8, vel=100, gain=0.6)
        parts.append(sec(s, 16))
    s = Song(186); s.add(BRASS, '[B2,F#3,B3,D4,F#4]:1 r:1 [B2,F#3,B3,D4,F#4]:2', vel=127); s.add(TIMP, 'B1:0.125 ' * 16 + 'B1:2', vel=120)
    s.drum({CRASH: 'x...x...'}, 0, 1, 4, vel=120)
    parts.append(sec(s, 4))
    return finish(concat(parts), OUT + 'arena/rey_de_la_montana.ogg', 2.2, 0.25, rms=0.13)


def valquirias():
    # Wagner, La cabalgata de las valquirias (motivo; arreglo propio). Compas ternario compuesto.
    fig = lambda a, b, c, d: f'{a}:0.375 {b}:0.125 {c}:0.5 {d}:2 '
    m = (fig('F#3', 'B3', 'F#3', 'B3') + fig('D4', 'B3', 'D4', 'F#4') + 'r:0 ' + fig('B3', 'D4', 'B3', 'D4') + fig('F#4', 'D4', 'F#4', 'A4') +
         fig('D4', 'F#4', 'D4', 'F#4') + fig('A4', 'F#4', 'A4', 'C#5') + fig('A3', 'D4', 'A3', 'D4') + fig('F#4', 'D4', 'F#4', 'A4'))
    s = Song(96); t = 0
    for r in range(3):
        s.add(VIOLIN, rep('B4:0.125 C#5:0.125 ', 4 * 24), at=t, vel=70, gain=0.35)  # trinos
        s.add(STRINGS, rep('[B2,F#3,B3]:3', 2) + ' ' + rep('[D3,F#3,A3]:3', 2) + ' ' + rep('[B2,F#3,B3]:3', 2) + ' ' + rep('[D3,F#3,A3]:3', 2), at=t, vel=75, gain=0.5)
        s.add(HORN, m, at=t, vel=100, gain=0.9)
        s.add(TROMBONE, m, at=t, vel=95, gain=0.7, transpose=-12)
        if r >= 1: s.add(TRUMPET, m, at=t, vel=100, gain=0.6, transpose=12)
        if r >= 1: s.add(TUBA, rep('B1:3 ', 2) + rep('D2:3 ', 2) + rep('B1:3 ', 2) + rep('D2:3 ', 2), at=t, vel=90, gain=0.6)
        s.add(TIMP, rep('B1:0.5 r:2.5 ', 8), at=t, vel=95, gain=0.6)
        if r == 2: s.drum({CRASH: 'x.....', SNARE: '...x..'}, t, 8, 3, vel=100, gain=0.5)
        t += 24
    s.add(BRASS, '[B2,F#3,B3,D4,F#4]:4', at=t, vel=120); s.drum({CRASH: 'x...'}, t, 1, 4, vel=120)
    return finish(concat([sec(s, t + 4)]), OUT + 'arena/cabalgata_valquirias.ogg', 2.4, 0.27, rms=0.13)


def combate(path=OUT + 'arena/tambores_de_guerra.ogg', key='D', bpm=150, seed=21, boss=False):
    rs = np.random.RandomState(seed)
    ch = ['Dm', 'Dm', 'Bb', 'C', 'Dm', 'Dm', 'Gm', 'A'] if not boss else ['Cm', 'Ab', 'Fm', 'G', 'Cm', 'Db', 'Bb', 'G']
    off = 0
    s = Song(bpm); t = 0
    sc = [62, 64, 65, 67, 69, 70, 72, 74, 76, 77] if not boss else [60, 62, 63, 65, 67, 68, 71, 72, 74, 75]
    for r in range(6):
        lvl = min(r, 4)
        s.add(STRINGS, ' '.join(rep(tok([chord(c, 3)[0]], 0.25) + ' ' + tok([chord(c, 3)[0] + 12], 0.25), 8) for c in ch), at=t, vel=75 + lvl * 5, gain=0.5, legato=0.5)
        s.add(CBASS, ' '.join(rep(tok([chord(c, 2)[0]], 0.5), 8) for c in ch), at=t, vel=90, gain=0.7, legato=0.5)
        s.add(TAIKO, rep('D2:0.75 D2:0.25 r:0.5 D2:0.5 D2:1 D2:0.5 D2:0.5', 8), at=t, vel=100, gain=0.8)
        s.drum({KICK: 'x...x...x...x.x.', SNARE: '....x.......x...' if lvl >= 1 else '................', HHC: 'x.x.x.x.x.x.x.x.' if lvl >= 2 else '................'}, t, 8, 4, vel=95, gain=0.55)
        if lvl >= 1: s.add(BRASS if not boss else TROMBONE, block(ch, 4, 3), at=t, vel=85, gain=0.5)
        if lvl >= 2: s.add(HORN, rand_melody(rs, sc, 12, [1, 2, 2, 3, 4]), at=t, vel=100, gain=0.8, transpose=-12)
        if lvl >= 3 or boss: s.add(CHOIR, block(ch, 4, 4), at=t, vel=85, gain=0.5)
        if lvl >= 4: s.add(TRUMPET, rand_melody(rs, sc, 16, [0.5, 1, 1, 2]), at=t, vel=100, gain=0.6)
        if r % 2 == 1: s.drum({CRASH: 'x' + '.' * 15}, t, 1, 4, vel=110, gain=0.6)
        t += 32
    s.add(BRASS, tok(chord(ch[0], 3), 4), at=t, vel=120); s.add(TIMP, 'D2:0.125 ' * 8 + 'D2:3', at=t, vel=120)
    return finish(concat([sec(s, t + 4)]), path, 1.8, 0.22, rms=0.13)


def jefe():
    return combate(OUT + 'arena/furia_del_coloso.ogg', bpm=168, seed=33, boss=True)


def victoria_arena():
    s = Song(126)
    s.add(BRASS, '[C4,E4,G4]:1 [C4,E4,G4]:0.5 [C4,E4,G4]:0.5 [D4,F4,A4]:1 [E4,G4,C5]:3', vel=115)
    s.add(TRUMPET, 'G5:1 G5:0.5 G5:0.5 A5:1 C6:3', vel=115)
    s.add(TIMP, 'C2:1 C2:0.5 C2:0.5 F1:1 C2:0.125 C2:0.125 C2:0.125 C2:0.125 C2:2.5', vel=115, gain=0.8)
    s.drum({CRASH: 'x.......x...', SNARE: '....xxxx....'}, 0, 1, 6, vel=110, gain=0.5)
    s.add(STRINGS, '[C3,G3,C4,E4]:6', vel=95)
    return finish(concat([sec(s, 7)]), OUT + 'arena/victoria.ogg', 2.4, 0.28, fade_out=2.0, rms=0.13)


def espera_arena():
    s = Song(80); t = 0
    for r in range(4):
        s.add(TAIKO, rep('D2:1 r:1 D2:0.5 D2:0.5 r:1', 8), at=t, vel=80, gain=0.6)
        s.add(CBASS, 'D2:8 C2:8 Bb1:8 A1:8', at=t, vel=70, gain=0.6)
        s.add(PADSWEEP, '[D3,A3]:8 [C3,G3]:8 [Bb2,F3]:8 [A2,E3]:8', at=t, vel=60, gain=0.4)
        if r >= 2: s.add(HORN, 'D4:4 F4:4 E4:4 A3:4 D4:4 G4:4 F4:4 E4:4', at=t, vel=75, gain=0.5, transpose=-12)
        t += 32
    return finish(concat([sec(s, t)]), OUT + 'arena/antesala.ogg', 3.0, 0.3, rms=0.1)


# ---------------- PUEBLO / GREMIO ----------------
def manana():
    # Grieg, La manana (Peer Gynt; arreglo propio). 6/8 -> negra con puntillo = 1.5
    m = ("G#5:1 F#5:0.5 E5:1 D#5:0.5 E5:1 F#5:0.5 G#5:1 F#5:0.5 E5:1 D#5:0.5 E5:1 F#5:0.5 E5:1 F#5:0.5 G#5:1 E5:0.5 "
         "G#5:1 A5:0.5 G#5:1 A5:0.5 B5:1 G#5:0.5 B5:1 G#5:0.5 A5:1 G#5:0.5 A5:1 B5:0.5 C#6:1.5 B5:1.5 ")
    ch = ['E', 'E', 'E', 'E', 'E', 'E', 'A', 'E']
    s = Song(66); t = 0
    for i, (lead, tr) in enumerate([(FLUTE, 0), (OBOE, 0), (FLUTE, 0), (VIOLIN, -12), (STRINGS, 0), (FLUTE, 0)]):
        s.add(lead, m, at=t, vel=88, gain=0.9, transpose=tr)
        s.add(SLOWSTR, block(ch, 3, 3), at=t, vel=50 + i * 4, gain=0.35)
        s.add(HARP, arp(ch, [0, 1, 2, 3, 2, 1], 0.5, 3), at=t, vel=55, gain=0.4)
        if i >= 3: s.add(HORN, block(ch, 3, 3), at=t, vel=60, gain=0.35)
        t += 24
    s.add(STRINGS, '[E3,B3,E4,G#4]:4', at=t, vel=80); s.add(FLUTE, 'E5:4', at=t, vel=80)
    return finish(concat([sec(s, t + 4)]), OUT + 'pueblo/la_manana_grieg.ogg', 2.8, 0.32, rms=0.1)


def gymnopedie():
    # Satie, Gymnopedie n.1 (arreglo propio)
    lh = lambda r, c: f'{r}:1 [{c}]:2 '
    acc = [('G2', 'B3,D4,F#4'), ('D2', 'A3,C#4,F#4')] * 2
    mel = ("r:3 r:3 r:3 r:3 F#5:1 A5:1 G5:1 F#5:1 C#5:1 B4:1 C#5:1 D5:1 A4:1 F#4:3 F#4:3 F#4:3 F#4:3 "
           "F#5:1 A5:1 G5:1 F#5:1 C#5:1 B4:1 C#5:1 D5:1 A4:1 C#5:3 F#5:3 E5:3 E5:3 ")
    nb = 17
    s = Song(70); t = 0
    for r in range(3):
        s.add(PIANO, ''.join(lh(*acc[k % 4]) for k in range(nb)), at=t, vel=60, gain=0.8, rel=2.0)
        s.add(PIANO if r != 1 else FLUTE, mel, at=t, vel=72, gain=0.9, rel=2.0)
        if r == 2: s.add(SLOWSTR, ''.join(f'[{acc[k % 4][1]}]:3 ' for k in range(nb)), at=t, vel=40, gain=0.25)
        t += nb * 3
    return finish(concat([sec(s, t)]), OUT + 'pueblo/gymnopedie_satie.ogg', 3.0, 0.32, rms=0.09)


def gremio_ambiente():
    return balada(OUT + 'pueblo/hogar_del_gremio.ogg') if False else _gremio()


def _gremio():
    rs = np.random.RandomState(9)
    ch = ['G', 'Em', 'C', 'D', 'G', 'C', 'Am', 'D']
    s = Song(88); t = 0
    for r in range(4):
        s.add(NYLON, arp(ch, [0, 2, 1, 2, 3, 2], 0.5, 3), at=t, vel=62, gain=0.6)
        s.add(ABASS, ' '.join(tok([chord(c, 2)[0]], 3) for c in ch), at=t, vel=65, gain=0.5)
        if r >= 1: s.add(RECORDER if r % 2 else DULCIMER, rand_melody(rs, [67, 69, 71, 72, 74, 76, 78, 79], 12, [1, 1, 2, 3]), at=t, vel=70, gain=0.5)
        t += 24
    return finish(concat([sec(s, t)]), OUT + 'pueblo/hogar_del_gremio.ogg', 1.8, 0.2, rms=0.09)


def noche():
    rs = np.random.RandomState(13)
    s = Song(50); t = 0
    for r in range(4):
        s.add(PADHALO, '[A2,E3,B3]:8 [F2,C3,G3]:8', at=t, vel=55, gain=0.5)
        s.add(MUSICBOX if r % 2 else CELESTA, rand_melody(rs, [69, 71, 72, 74, 76, 79, 81], 10, [1, 1.5, 2]), at=t, vel=55, gain=0.45)
        s.add(HARP, 'A2:4 E3:4 F2:4 C3:4', at=t, vel=50, gain=0.4)
        t += 16
    return finish(concat([sec(s, t)]), OUT + 'pueblo/noche_estrellada.ogg', 4.0, 0.45, rms=0.08)


ALL = [toccata, dies_irae, claro_luna, ambiente_dragon, cripta,
       scarborough, marinero, oda_alegria, jiga, balada, greensleeves_laud,
       mision_inicio, mision_completada, mision_fallida, descubrimiento, misterio, viaje, triste,
       rey_montana, valquirias, combate, jefe, victoria_arena, espera_arena,
       manana, gymnopedie, gremio_ambiente, noche]
