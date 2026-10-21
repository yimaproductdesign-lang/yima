"""Synthesised, licence-free sound bed: soft pad + word ticks + scene whooshes/thumps. Pure numpy.
This is a placeholder-quality bed. For reach, add a licensed/trending track inside Instagram and keep this as sfx, or replace the pad."""
import wave
import numpy as np

SR = 44100
ROOTS = [110.0, 123.47, 98.0, 110.0, 130.81, 110.0, 98.0, 110.0]  # per-scene pad root (A2, B2, G2 ...)


def _env(n, a, d):
    t = np.arange(n) / SR
    return np.minimum(1, t / a) * np.exp(-t / d)


def _add(buf, x, t0, gain=1.0):
    i = int(t0 * SR)
    if i >= len(buf): return
    j = min(len(buf), i + len(x)); buf[i:j] += x[: j - i] * gain


def _lp(x, k):
    c = np.cumsum(np.insert(x, 0, 0)); y = (c[k:] - c[:-k]) / k
    return np.concatenate([np.zeros(k - 1), y])


def synth(scenes, total, path):
    rng = np.random.default_rng(7)
    n = int((total + 0.4) * SR)
    t = np.arange(n) / SR
    pad = np.zeros(n)
    for si, s in enumerate(scenes):
        a, b = int(s["start"] * SR), min(n, int(s["end"] * SR))
        r = ROOTS[si % len(ROOTS)]
        seg = np.zeros(b - a); tt = np.arange(b - a) / SR
        for mult, g in ((1, .5), (1.5, .35), (2, .3), (2.5, .15)):
            seg += g * np.sin(2 * np.pi * r * mult * tt + 0.3 * np.sin(2 * np.pi * 0.2 * tt))
        w = min(1, 1)  # cross-fade scene pads
        f = int(0.35 * SR); env = np.ones(b - a); env[:f] = np.linspace(0, 1, f); env[-f:] = np.linspace(1, 0, f)
        pad[a:b] += seg * env
    pad *= 0.045
    fx = np.zeros(n)
    for si, s in enumerate(scenes):
        for ln in s["lines"]:
            for k, w in enumerate(ln["words"]):
                t0 = s["start"] + w["t"]
                f0 = [660, 740, 880, 990][(k + si) % 4]
                m = int(0.25 * SR); tt = np.arange(m) / SR
                blip = np.sin(2 * np.pi * f0 * tt) * _env(m, .002, .05) * 0.5
                click = (rng.standard_normal(m) * _env(m, .0005, .006)) * 0.25
                _add(fx, blip + click, t0, 0.10)
        if si > 0:  # cut: low thump + short whoosh
            m = int(0.9 * SR); tt = np.arange(m) / SR
            thump = np.sin(2 * np.pi * (60 - 20 * tt) * tt) * _env(m, .005, .22)
            _add(fx, thump, s["start"], 0.30)
            m2 = int(0.4 * SR); noise = _lp(rng.standard_normal(m2), 40)
            sw = noise * np.sin(np.pi * np.arange(m2) / m2) ** 2
            _add(fx, sw / (np.abs(sw).max() + 1e-9), s["start"] - 0.28, 0.16)
    # simple echo on fx for space
    d = int(0.21 * SR); echo = np.zeros(n); echo[d:] = fx[:-d] * 0.32
    mix = pad + fx + echo
    fade = int(1.0 * SR); mix[-fade:] *= np.linspace(1, 0, fade); mix[: int(0.05 * SR)] *= np.linspace(0, 1, int(0.05 * SR))
    mix = mix / (np.abs(mix).max() + 1e-9) * 0.7   # peak about -3 dBFS
    pcm = (np.clip(mix, -1, 1) * 32767).astype("<i2")
    with wave.open(str(path), "wb") as wf:
        wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(SR); wf.writeframes(pcm.tobytes())
