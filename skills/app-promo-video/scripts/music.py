import os, sys, wave
import numpy as np
from scipy.signal import butter, sosfilt, fftconvolve

SR = 48000
BPM = 128  # same grid as the edit; the groove is half-time, so it feels like 64
BEAT = 60 / BPM
BAR = 4 * BEAT
BARS = int(os.environ.get("BARS", "24"))  # length: BARS × 1.875 s
N = int(SR * BAR * BARS)
rng = np.random.default_rng(11)
OUT = sys.argv[1] if len(sys.argv) > 1 else "calm.wav"
END = BARS - 2  # final chord under the outro
FULL = int(os.environ.get("FULL", "14"))  # bar where the second bell voice joins


def note(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def tt(dur):
    return np.arange(int(dur * SR)) / SR


def lp(x, f, order=2):
    return sosfilt(butter(order, min(f, SR * 0.45), "low", fs=SR, output="sos"), x, axis=0)


def hp(x, f, order=2):
    return sosfilt(butter(order, f, "high", fs=SR, output="sos"), x, axis=0)


class Bus:
    def __init__(self):
        self.x = np.zeros((N, 2))

    def add(self, sig, t, gain=1.0, pan=0.0):
        i = int(round(t * SR))
        if i >= N or i < 0:
            return
        if sig.ndim == 1:
            sig = np.stack([sig * min(1, 1 - pan), sig * min(1, 1 + pan)], 1)
        sig = sig[: N - i]
        self.x[i : i + len(sig)] += sig * gain


pads, keys, bass, drums, bells = Bus(), Bus(), Bus(), Bus(), Bus()

# D major, warm and open: Dmaj9 - Bm9 - Gmaj9 - A6/9 (sus-ish)
CHORDS = [[50, 54, 57, 61, 64], [47, 50, 54, 57, 61], [43, 47, 50, 54, 57], [45, 49, 52, 54, 59]]
ROOTS = [38, 35, 31, 33]


def env(n, a, r):
    e = np.ones(n)
    ai = int(a * SR)
    ri = int(r * SR)
    if ai:
        e[:ai] = np.linspace(0, 1, ai) ** 2
    if ri:
        e[-ri:] *= np.linspace(1, 0, ri) ** 2
    return e


def pad_voice(m, dur):
    t = tt(dur)
    l = np.zeros_like(t)
    r = np.zeros_like(t)
    for d in (-0.004, 0.0, 0.004):
        ph = rng.random()
        s = 2 * ((t * note(m) * (1 + d) + ph) % 1) - 1
        l += s * (0.7 - 40 * d)
        r += s * (0.7 + 40 * d)
    x = np.stack([l, r], 1) / 3
    return lp(x, 1100, 2)


def epiano(m, dur, vel=1.0):
    t = tt(dur + 1.2)
    f = note(m)
    body = np.sin(2 * np.pi * f * t + 0.6 * np.sin(2 * np.pi * f * t) * np.exp(-t * 6))
    tine = 0.25 * np.sin(2 * np.pi * f * 4.02 * t) * np.exp(-t * 9)
    e = np.exp(-t * 2.2) * env(len(t), 0.004, 0.25)
    return (body + tine) * e * vel


def bell(m, dur=1.6):
    t = tt(dur)
    f = note(m)
    x = np.sin(2 * np.pi * f * t) + 0.35 * np.sin(2 * np.pi * f * 2.76 * t) * np.exp(-t * 4) + 0.15 * np.sin(2 * np.pi * f * 5.4 * t) * np.exp(-t * 8)
    return x * np.exp(-t * 2.6) * env(len(t), 0.002, 0.2)


def soft_kick():
    t = tt(0.5)
    f = 42 + 70 * np.exp(-t * 30)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 7) * 0.9


def rim():
    t = tt(0.12)
    x = np.sin(2 * np.pi * 1650 * t) * np.exp(-t * 60) * 0.4 + hp(rng.standard_normal(len(t)), 2000) * np.exp(-t * 80) * 0.25
    return x


def shaker():
    t = tt(0.09)
    x = hp(rng.standard_normal(len(t)), 6000, 4)
    e = np.minimum(t / 0.015, 1) * np.exp(-t * 35)
    return x * e * 0.35


def swell(dur):
    n = int(dur * SR)
    x = hp(lp(rng.standard_normal((n, 2)), 3500), 400)
    return x * ((np.arange(n) / n) ** 3)[:, None] * 0.6


# pads: whole piece, opening slowly
for bar in range(BARS - 1):
    ch = CHORDS[bar % 4]
    dur = BAR + 0.6
    x = sum(pad_voice(m, dur) for m in ch) / len(ch)
    x *= env(len(x), 0.5, 0.9)[:, None]
    g = 0.5 if bar < 2 else 0.42
    if bar >= END:
        g = 0.0
    pads.add(x, bar * BAR, g)

# electric piano: soft chord on 1, gentle push on the "and" of 2 — leaves room for the clicks
for bar in range(1, END):
    ch = CHORDS[bar % 4]
    for t0, vel, top in ((0, 1.0, 4), (1.5 * BEAT, 0.55, 3), (3 * BEAT, 0.45, 2)):
        if bar == 1 and t0 > 0:
            continue
        for k, m in enumerate(ch[1:top + 1]):
            keys.add(epiano(m + 12, BEAT * 1.5, vel * 0.5), bar * BAR + t0 + k * 0.012, 0.22, -0.2 + 0.13 * k)

# bass: long notes, a small pickup at the end of each bar
for bar in range(2, END):
    r = ROOTS[bar % 4]
    t = tt(BAR + 0.25)
    x = np.sin(2 * np.pi * note(r) * t) + 0.25 * np.sin(2 * np.pi * note(r) * 2 * t)
    x *= env(len(t), 0.06, 0.3) * (0.8 + 0.2 * np.exp(-t * 2))
    bass.add(x, bar * BAR, 0.24)

# half-time groove: kick on 1, rim on 3, shaker eighths
for bar in range(2, END):
    b0 = bar * BAR
    drums.add(soft_kick(), b0, 0.55)
    if bar % 2 == 1:
        drums.add(soft_kick(), b0 + 2.5 * BEAT, 0.3)
    drums.add(rim(), b0 + 2 * BEAT, 0.5, 0.1)
    for k in range(8):
        if bar < 4 and k % 2 == 0:
            continue
        drums.add(shaker(), b0 + k * BEAT / 2, 0.25 + (0.12 if k % 2 else 0), 0.35)

# bell melody: sparse, from bar 6, a little fuller after bar 10
MEL = [
    [(0, 74), (3, 76), (6, 73)],
    [(0, 71), (4, 69)],
    [(0, 74), (2, 71), (5, 67)],
    [(0, 69), (3, 71), (6, 73)],
]
for bar in range(6, END):
    for e8, m in MEL[bar % 4]:
        bells.add(bell(m + 12), bar * BAR + e8 * BEAT / 2, 0.16, 0.25)
        if bar >= FULL:
            bells.add(bell(m), bar * BAR + e8 * BEAT / 2 + 0.006, 0.08, -0.25)

pads.add(swell(BAR), 1 * BAR, 0.18)
pads.add(swell(BAR), (FULL - 1) * BAR, 0.14)

# ending: one sustained chord with a bell arpeggio that rings out
ch = CHORDS[0]
x = sum(pad_voice(m, BAR * 2) for m in ch + [ch[0] + 12]) / 5
x *= env(len(x), 0.05, 2.2)[:, None]
pads.add(x, END * BAR, 0.6)
for k, m in enumerate(ch[1:] + [ch[0] + 24]):
    keys.add(epiano(m + 12, BAR, 0.6), END * BAR + k * BEAT / 2, 0.25, -0.3 + 0.15 * k)
    bells.add(bell(m + 24, 2.5), END * BAR + k * BEAT / 2, 0.08, 0.3 - 0.15 * k)
t = tt(3.0)
bass.add(np.sin(2 * np.pi * note(ROOTS[0]) * t) * np.exp(-t * 1.2), END * BAR, 0.32)
drums.add(soft_kick(), END * BAR, 0.5)

# gentle sidechain so the kick breathes
side = np.ones(N)
for bar in range(2, END + 1):
    i = int(bar * BAR * SR)
    n = min(int(BEAT * 1.2 * SR), N - i)
    side[i : i + n] = np.minimum(side[i : i + n], 0.65 + 0.35 * np.linspace(0, 1, n) ** 0.7)

ir_t = tt(2.8)
ir = rng.standard_normal((len(ir_t), 2)) * np.exp(-ir_t * 2.0)[:, None]
ir = lp(ir, 5000)
ir /= np.sqrt((ir ** 2).sum(0))
send = hp(keys.x * 0.6 + bells.x * 0.9 + pads.x * 0.3 + drums.x * 0.1, 250)
rev = np.stack([fftconvolve(send[:, c], ir[:, c])[:N] for c in range(2)], 1)

mix = (pads.x + bass.x) * side[:, None] + keys.x + bells.x + drums.x + rev * 0.45
mix = hp(mix, 30)
mix /= np.abs(mix).max()
mix = np.tanh(mix * 1.3) / np.tanh(1.3)
fi = int(0.8 * SR)
mix[:fi] *= (np.linspace(0, 1, fi) ** 2)[:, None]
fo = int(1.2 * SR)
mix[-fo:] *= (np.linspace(1, 0, fo) ** 2)[:, None]
mix /= np.abs(mix).max() / 0.9

with wave.open(OUT, "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes((mix * 32767).astype("<i2").tobytes())
print("seconds", N / SR)
