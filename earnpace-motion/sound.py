"""Synthesised sound design for EarnPace — Set Your Pace. Cues match index.html's timeline."""
import sys, wave
import numpy as np

SR, DUR = 48000, 18.5
N = int(SR * DUR)
rng = np.random.default_rng(4)
L = np.zeros(N); Rt = np.zeros(N)
t_all = np.arange(N) / SR

def add(sig, at, pan=0.0, gain=1.0):
    i = int(at * SR); j = min(N, i + len(sig))
    if j <= i: return
    s = sig[: j - i] * gain
    L[i:j] += s * np.sqrt((1 - pan) / 2) * 1.414
    Rt[i:j] += s * np.sqrt((1 + pan) / 2) * 1.414

def env(n, a, d):  # attack/exp-decay envelope, seconds
    t = np.arange(n) / SR
    return np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / d)

def lowpass(x, cut):
    a = np.exp(-2 * np.pi * cut / SR); y = np.zeros_like(x); acc = 0.0
    for i, v in enumerate(x): acc = (1 - a) * v + a * acc; y[i] = acc
    return y

def tone(f, dur, a=.005, d=.4, harm=(1, .5, .25, .12)):
    n = int(dur * SR); t = np.arange(n) / SR
    s = sum(h * np.sin(2 * np.pi * f * (k + 1) * t) * np.exp(-t * k * 3) for k, h in enumerate(harm))
    return s * env(n, a, d)

def whoosh(dur, rise=True, cut0=300, cut1=6000):
    n = int(dur * SR); x = rng.standard_normal(n)
    t = np.linspace(0, 1, n); shape = np.sin(np.pi * (t ** (0.75 if rise else 1.35))) ** 2
    # sweep a one-pole lowpass by blocks
    out = np.zeros(n); acc = 0.0; blk = 256
    for b in range(0, n, blk):
        k = b / n; cut = cut0 + (cut1 - cut0) * (k if rise else 1 - k)
        a = np.exp(-2 * np.pi * cut / SR)
        for i in range(b, min(n, b + blk)): acc = (1 - a) * x[i] + a * acc; out[i] = acc
    return out * shape / (np.abs(out).max() + 1e-9)

def thump(f0=110, dur=.35):
    n = int(dur * SR); t = np.arange(n) / SR
    f = f0 * (1 + 1.5 * np.exp(-t * 40)); ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * env(n, .002, .09)

def tick():
    n = int(.03 * SR); x = rng.standard_normal(n); x = x - lowpass(x, 3000)
    return x * env(n, .0005, .006)

# ---- scene 1: tension -------------------------------------------------------
for k, at in enumerate(np.arange(0.15, 2.85, 0.125)):
    add(tick(), at, pan=np.sin(k * 1.7) * .5, gain=.22 + .1 * (k % 2))
drone_n = int(3.4 * SR); dt = np.arange(drone_n) / SR
drone = (np.sin(2 * np.pi * 55 * dt) + .5 * np.sin(2 * np.pi * 58.3 * dt) + .3 * np.sin(2 * np.pi * 110.7 * dt))
drone *= np.minimum(1, dt / .6) * np.clip((3.4 - dt) / .7, 0, 1)
add(drone, 0, gain=.16)
add(whoosh(.9, True, 200, 4000), 0.25, gain=.18)               # headline
add(whoosh(1.0, False, 3000, 150), 2.8, gain=.32)              # chaos settles

# ---- scene 2: calm pulse ----------------------------------------------------
for k in range(4):
    add(thump(90, .45), 3.95 + k * .6, gain=.55)
pad_n = int((DUR - 3.3) * SR); pt = np.arange(pad_n) / SR
chord = [130.81, 196.0, 261.63, 293.66, 392.0]                 # C add9, warm
pad = sum(np.sin(2 * np.pi * f * pt + i) * (1 + .3 * np.sin(2 * np.pi * .3 * pt + i)) for i, f in enumerate(chord))
pad = lowpass(pad, 1400)
pad *= np.minimum(1, pt / 1.2) * np.clip((pad_n / SR - pt) / 1.0, 0, 1)
pad *= 1 + .6 * np.clip((pt - 8.5) / 1.5, 0, 1) * np.clip((11.9 - pt) / 1, 0.4, 1)   # swell under zoom-out
add(pad, 3.3, gain=.045)

# ---- scene 3: hops + landings (ascending C E G C) ---------------------------
ARR = [6.6, 8.1, 9.6, 11.1]; NOTES = [523.25, 659.25, 783.99, 1046.5]
for i, a in enumerate(ARR):
    add(whoosh(.5, True, 400, 3500), a - .55, pan=-.2, gain=.12)
    add(tone(NOTES[i], 1.6, d=.55), a, pan=(i - 1.5) * .2, gain=.3)
    add(tone(NOTES[i] / 2, 1.0, d=.25, harm=(1, .3)), a, gain=.18)
    add(thump(70, .3), a, gain=.35)

# ---- scene 4: zoom out + rising curve ---------------------------------------
add(whoosh(1.3, True, 150, 5000), 11.75, gain=.35)
gn = int(1.9 * SR); gt = np.arange(gn) / SR
gl = np.sin(2 * np.pi * np.cumsum(400 * 2 ** (gt / 1.9 * 1.5)) / SR) * np.sin(np.pi * gt / 1.9) ** 2
add(gl, 12.4, gain=.05)
for k, at in enumerate(np.linspace(12.25, 12.9, 6)):              # bars popping up
    add(tone(1046.5 * 2 ** (k / 12 * 2), .3, d=.08, harm=(1, .2)), at, pan=-.4 + k * .16, gain=.1)

# ---- transition + brand -----------------------------------------------------
rn = int(1.0 * SR); rt = np.arange(rn) / SR
rev = rng.standard_normal(rn); rev = rev - lowpass(rev, 1500); rev *= (rt / 1.0) ** 3
add(rev, 14.25, gain=.22)                                          # reverse-cymbal swell into reveal
add(thump(55, .8), 15.2, gain=.8)
add(whoosh(.8, False, 5000, 300), 15.2, gain=.25)
for f in [523.25, 659.25, 783.99, 987.77, 1174.66]:                  # logo chord on dot pop
    add(tone(f, 2.6, a=.01, d=1.1), 15.95, gain=.09)
add(tone(1567.98, 1.2, d=.3), 15.95, gain=.08)
add(tone(1318.5, .8, d=.2, harm=(1, .2)), 17.05, gain=.12)           # url pill

# ---- reverb + master ----------------------------------------------------------
def reverb(x, secs=1.6, mix=.22):
    ir_n = int(secs * SR); ir = rng.standard_normal(ir_n) * np.exp(-np.arange(ir_n) / SR / (secs / 5))
    ir = lowpass(ir, 5000); ir /= np.sqrt((ir ** 2).sum())
    m = 1 << int(np.ceil(np.log2(len(x) + ir_n)))
    wet = np.fft.irfft(np.fft.rfft(x, m) * np.fft.rfft(ir, m), m)[: len(x)]
    return x + wet * mix
L, Rt = reverb(L), reverb(Rt)
fade = np.clip((DUR - t_all) / .6, 0, 1); L *= fade; Rt *= fade
st = np.stack([L, Rt], 1); st = np.tanh(st / np.abs(st).max() * 1.2) ; st *= .89 / np.abs(st).max()
with wave.open(sys.argv[1], 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((st * 32767).astype('<i2').tobytes())
print('ok', st.shape)
