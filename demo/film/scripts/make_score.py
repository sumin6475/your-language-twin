"""Ambient score for the Language Role Model demo film.

Restrained cinematic bed: detuned sine-cluster pads, low sub drone,
felt-piano motif, high shimmer — volume/brightness automated to the
film's 9-beat arc. Deterministic (fixed seed), 178 s, 44.1 kHz stereo.
"""
import numpy as np
import soundfile as sf

SR = 44100
DUR = 178.0
N = int(SR * DUR)
t = np.arange(N) / SR
rng = np.random.default_rng(7)

def note(f):
    return f

A2, C3, D3, E3, F3, G3 = 110.0, 130.81, 146.83, 164.81, 174.61, 196.0
A3, B3, C4, E4, G4, B4 = 220.0, 246.94, 261.63, 329.63, 392.0, 493.88
A4, C5, D5, E5, G5 = 440.0, 523.25, 587.33, 659.26, 783.99

# ---- chord progression: Am9 -> Fmaj9 -> Cmaj9 -> G6, 16 s each, looped
CHORDS = [
    [A2, E3, A3, C4, E4, B4],          # Am9 (B4 = 9th)
    [F3, C4, A3, E4, G4, A4],          # Fmaj9-ish
    [C3, G3, E4, B3, G4, D5],          # Cmaj9
    [G3, D3, B3, G4, B4, E5],          # G6
]
SEG = 16.0

def env_lookup(points, tt):
    """Piecewise-linear envelope from (time, value) pairs."""
    xs = np.array([p[0] for p in points])
    ys = np.array([p[1] for p in points])
    return np.interp(tt, xs, ys)

# global intensity arc (film acts)
master = env_lookup([
    (0, 0.10), (12, 0.16), (22, 0.22), (36, 0.26), (60, 0.30),
    (80, 0.42), (98, 0.48), (120, 0.55), (135, 0.72), (150, 0.80),
    (162, 0.60), (170, 0.40), (175, 0.12), (178, 0.0)], t)
# brightness arc controls upper-partial level
bright = env_lookup([
    (0, 0.05), (22, 0.15), (80, 0.35), (135, 0.8), (162, 0.5), (178, 0.2)], t)

L = np.zeros(N)
R = np.zeros(N)

# ---- pads --------------------------------------------------------------
def pad_voice(freq, seg_start, seg_len, detune, pan):
    n0, n1 = int(seg_start * SR), int(min((seg_start + seg_len), DUR) * SR)
    if n1 <= n0:
        return
    tt = np.arange(n1 - n0) / SR
    seg = np.zeros(n1 - n0)
    for k, amp in [(1, 1.0), (2, 0.35), (3, 0.12)]:
        ph = rng.uniform(0, 2 * np.pi)
        seg += amp * np.sin(2 * np.pi * freq * k * (1 + detune) * tt + ph)
    # slow attack / release within segment, overlapping crossfade feel
    a = np.clip(tt / 5.0, 0, 1)
    r = np.clip((seg_len - tt) / 5.0, 0, 1)
    lfo = 1 + 0.12 * np.sin(2 * np.pi * 0.11 * tt + rng.uniform(0, 6.28))
    seg *= a * r * lfo
    gl = np.sqrt(0.5 * (1 - pan))
    gr = np.sqrt(0.5 * (1 + pan))
    L[n0:n1] += seg * gl
    R[n0:n1] += seg * gr

n_segs = int(np.ceil(DUR / SEG))
for i in range(n_segs):
    chord = CHORDS[i % 4]
    start = i * SEG
    for j, f in enumerate(chord):
        # lower voices centered, upper voices spread + gated by brightness later
        pan = [-0.1, 0.1, -0.35, 0.35, -0.6, 0.6][j % 6]
        det = rng.uniform(-0.0015, 0.0015)
        lvl = [0.5, 0.4, 0.32, 0.26, 0.16, 0.13][j]
        pad_voice(f, start, SEG + 4.0, det, pan)  # +4 s overlap
        # scale afterwards via per-voice level: cheat — apply now
# normalize pad cluster roughly
pad_norm = max(np.max(np.abs(L)), np.max(np.abs(R))) + 1e-9
L /= pad_norm
R /= pad_norm

# split pads into low/high halves for brightness control is complex; instead
# apply gentle one-pole lowpass whose cutoff follows `bright`
def onepole_lp(x, cutoff_hz):
    y = np.zeros_like(x)
    alpha = np.clip(2 * np.pi * cutoff_hz / SR, 0.0005, 0.5)
    acc = 0.0
    for idx in range(0, len(x), 4096):
        blk = x[idx:idx + 4096]
        a = alpha[idx] if hasattr(alpha, "__len__") else alpha
        for i2, v in enumerate(blk):
            acc += a * (v - acc)
            y[idx + i2] = acc
    return y

cut = 400 + 3600 * bright  # Hz
L = onepole_lp(L, cut)
R = onepole_lp(R, cut)

# ---- sub drone ---------------------------------------------------------
sub_f = env_lookup([(0, 55.0), (162, 55.0), (163, 55.0), (178, 55.0)], t)
sub = 0.5 * np.sin(2 * np.pi * np.cumsum(sub_f) / SR)
sub *= env_lookup([(0, 0.5), (22, 0.35), (80, 0.45), (162, 0.5), (172, 0.2), (178, 0)], t)
L += sub * 0.5
R += sub * 0.5

# ---- felt piano motif --------------------------------------------------
def felt_note(freq, start, dur=3.2, vel=0.5, pan=0.0):
    n0 = int(start * SR)
    n1 = min(int((start + dur) * SR), N)
    if n1 <= n0:
        return
    tt = np.arange(n1 - n0) / SR
    envl = np.exp(-tt * 1.6) * np.minimum(tt / 0.012, 1)
    x = (np.sin(2 * np.pi * freq * tt) + 0.30 * np.sin(2 * np.pi * freq * 2 * tt)
         + 0.08 * np.sin(2 * np.pi * freq * 3 * tt))
    thump = 0.10 * np.exp(-tt * 40) * rng.standard_normal(len(tt))
    seg = (x * envl + thump) * vel
    gl = np.sqrt(0.5 * (1 - pan))
    gr = np.sqrt(0.5 * (1 + pan))
    L[n0:n1] += seg * gl * 0.32
    R[n0:n1] += seg * gr * 0.32

# motif: E5 . C5 . B4 A4 — enters at the signature scene (80 s), denser later
motif = [(0.0, E5, .55), (1.9, C5, .45), (4.1, B4, .40), (6.0, A4, .50)]
starts = [80, 96, 112, 128, 136, 144, 152, 160]
for s in starts:
    density = 1.0 if s < 135 else 1.0
    for (off, f, v) in motif:
        if s >= 152 and off > 4:      # thin the tail as we resolve
            continue
        felt_note(f, s + off, vel=v * (0.8 if s < 98 else 1.0),
                  pan=rng.uniform(-0.3, 0.3))
# answering low note each cycle
for s in [88, 104, 120, 140, 156]:
    felt_note(A3, s, dur=4.5, vel=0.4, pan=0)
# final resolution note
felt_note(A4, 168.5, dur=6.0, vel=0.5)
felt_note(E4, 170.5, dur=6.0, vel=0.35)

# ---- shimmer (high octave, fullest act only) ---------------------------
shim_env = env_lookup([(120, 0), (135, 0.5), (150, 0.6), (162, 0.25), (172, 0)], t)
shim = np.zeros(N)
for f in [A4 * 2, C5 * 2, E5 * 2]:
    ph = rng.uniform(0, 6.28)
    v = np.sin(2 * np.pi * f * t + ph) * (1 + 0.3 * np.sin(2 * np.pi * 0.07 * t + ph))
    shim += v
shim = shim / 3 * shim_env * 0.05
L += shim
R += shim * 0.9

# ---- master ------------------------------------------------------------
L *= master
R *= master
mix = np.stack([L, R], axis=1)
peak = np.max(np.abs(mix)) + 1e-9
mix = mix / peak * 0.5   # leave headroom; final loudness set in the film mix
sf.write("audio/score.wav", mix.astype(np.float32), SR)
print("score.wav written", mix.shape, "peak", float(np.max(np.abs(mix))))
