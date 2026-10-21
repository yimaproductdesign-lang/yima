"""Licence-free generative music bed, beat-synced to the reel. numpy + scipy only.
Moods: reflective (lo-fi, 88 bpm), pulse (minimal electronic, 104 bpm), dark (cinematic minor, 96 bpm).
Structure: filtered intro -> groove -> breakdown (no kick) with riser -> drop -> outro on the end card.
This is a generated bed, not a hit record. For maximum reach, swap in a trending track inside Instagram."""
import numpy as np
from scipy.signal import butter, lfilter

SR = 44100
MOODS = {
    "reflective": dict(bpm=88, prog=[(57, "m"), (53, "M"), (48, "M"), (55, "M")], swing=0.14,
                       kick=[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0], hats16=False, bass=[1, 0, 0, 1, 0, 0, 1, 0], arp_oct=12),
    "pulse": dict(bpm=104, prog=[(57, "m"), (57, "m"), (53, "M"), (55, "M")], swing=0.0,
                  kick=[1, 0, 0, 0] * 4, hats16=True, bass=[0, 1, 0, 1, 0, 1, 0, 1], arp_oct=12),
    "dark": dict(bpm=96, prog=[(50, "m"), (46, "M"), (53, "M"), (48, "M")], swing=0.06,
                 kick=[1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0], hats16=False, bass=[1, 0, 1, 0, 1, 0, 1, 1], arp_oct=12),
}


def hz(m): return 440.0 * 2 ** ((m - 69) / 12)


def chord(root, q): return [root, root + (3 if q == "m" else 4), root + 7]


def filt(x, f, kind="low", order=2):
    b, a = butter(order, f / (SR / 2), btype=kind)
    return lfilter(b, a, x)


def env(n, a, d):
    t = np.arange(n) / SR
    return np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / d)


def add(buf, x, t0, g=1.0):
    i = int(t0 * SR)
    if i < 0 or i >= len(buf): return
    j = min(len(buf), i + len(x)); buf[i:j] += x[: j - i] * g


rng = np.random.default_rng(11)


def kick():
    n = int(.45 * SR); t = np.arange(n) / SR
    f = 45 + 85 * np.exp(-t / .045)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, .001, .16)


def clap():
    n = int(.25 * SR); x = filt(rng.standard_normal(n), 1800, "high")
    e = env(n, .001, .07); e[: int(.012 * SR)] *= (np.sin(np.linspace(0, 9 * np.pi, int(.012 * SR))) ** 2)
    return x * e * .8 + np.sin(2 * np.pi * 190 * np.arange(n) / SR) * env(n, .001, .03) * .3


def hat(open_=False):
    n = int((.25 if open_ else .06) * SR)
    return filt(rng.standard_normal(n), 7000, "high") * env(n, .0005, .09 if open_ else .018)


def bass_note(m, dur):
    n = int(dur * SR); t = np.arange(n) / SR; f = hz(m)
    x = sum(np.sin(2 * np.pi * f * k * t) / k for k in range(1, 6))
    return filt(x, 420) * env(n, .004, dur * .7)


def pluck(m, dur=.35):
    n = int(dur * SR); t = np.arange(n) / SR; f = hz(m)
    return (np.sin(2 * np.pi * f * t) + .45 * np.sin(4 * np.pi * f * t) + .2 * np.sin(6 * np.pi * f * t)) * env(n, .002, .11)


def pad_chord(notes, dur):
    n = int(dur * SR); t = np.arange(n) / SR; x = np.zeros(n)
    for m in notes:
        for d in (-.0018, 0, .0018):
            x += np.sin(2 * np.pi * hz(m) * (1 + d) * t + rng.uniform(0, 6.28))
    e = np.minimum(1, t / .35) * np.minimum(1, (dur - t) / .4).clip(0)
    return filt(x, 1600) * e


def compose(total, mood="reflective", drop_at=None):
    M = MOODS[mood]; beat = 60 / M["bpm"]; step = beat / 4; bar = beat * 4
    nbars = int(np.ceil(total / bar)) + 1
    n = int((total + 1.5) * SR)
    drums, bassb, arpb, padb, fxb = (np.zeros(n) for _ in range(5))
    duck = np.ones(n)
    b_drop = int(round((drop_at or total * .55) / bar))
    breakdown = set(range(max(2, b_drop - 2), b_drop))
    outro_from = int((total - 2.6) // bar)
    for b in range(nbars):
        root, q = M["prog"][b % 4]; ch = chord(root, q); t_bar = b * bar
        intro, brk, outro = b < 2, b in breakdown, b >= outro_from
        padb_seg = pad_chord([c - 12 + 12 for c in ch], bar + .4); add(padb, padb_seg, t_bar, 1.0)
        for s in range(16):
            ts = t_bar + s * step + (M["swing"] * step if s % 2 else 0)
            if not (intro or brk or outro) and M["kick"][s]:
                add(drums, kick(), ts, 1.0)
                i = int(ts * SR); m = min(n - i, int(.3 * SR))
                if m > 0: duck[i:i + m] = np.minimum(duck[i:i + m], 1 - .55 * np.exp(-np.arange(m) / SR / .09))
            if not (intro or brk or outro) and s in (4, 12): add(drums, clap(), ts, .42)
            if not outro and (s % 2 == 0 or M["hats16"]):
                add(drums, hat(open_=(s == 14 and b % 2 == 1)), ts, (.10 if intro else .16) * (1 if s % 4 == 2 else .7))
            if not (intro or outro) and s % 2 == 0 and M["bass"][s // 2] and not brk:
                add(bassb, bass_note(ch[0] - 24, step * 1.8), ts, 1.0)
            if not outro and b >= 1:
                seq = [0, 1, 2, 1, 2, 0, 1, 2]
                if s % 2 == 0 or brk: add(arpb, pluck(ch[seq[s % 8]] + M["arp_oct"]), ts, .9 if brk else .7)
        if b == b_drop - 1:  # riser into the drop
            m = int(bar * SR); x = rng.standard_normal(m); k = np.linspace(0, 1, m) ** 2
            r = filt(x, 900, "high") * k * .5 + np.sin(2 * np.pi * np.cumsum(200 + 900 * k) / SR) * k * .15
            add(fxb, r, t_bar, .5)
        if b == b_drop:  # impact
            m = int(1.6 * SR); add(fxb, filt(rng.standard_normal(m), 3000) * env(m, .001, .5), t_bar, .35); add(fxb, kick(), t_bar, .9)
    # intro low-pass sweep on drums/arp
    i2 = int(2 * bar * SR)
    if i2 < n:
        drums[:i2] = filt(drums[:i2], 2500); arpb[:i2] = filt(arpb[:i2], 1800)
    mix = drums * .85 + bassb * .55 * duck + arpb * .16 * duck + padb * .055 * duck + fxb
    return mix, beat


def master(x, peak=.89):
    x = np.tanh(1.3 * x / (np.abs(x).max() + 1e-9)) / np.tanh(1.3)
    return x / (np.abs(x).max() + 1e-9) * peak
