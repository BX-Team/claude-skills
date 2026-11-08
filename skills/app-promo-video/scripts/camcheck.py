"""Prints the worst per-frame window jump and each segment's playback speed range for render.py's edit plan."""
import os, sys

sys.argv = sys.argv[:1]
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import render as r

prev, worst = None, (0.0, 0.0)
for i in range(int(r.INTRO_END * r.FPS), int(r.OUTRO_START * r.FPS)):
    v = i / r.FPS
    sg = r.seg_at(v)
    k = r.SEGMENTS.index(sg)
    p = r.place(sg, v)
    if k > 0 and sg["v0"] not in r.CONTINUOUS and v - sg["v0"] < r.XFADE:
        e = r.ease((v - sg["v0"]) / r.XFADE)
        a = r.place(r.SEGMENTS[k - 1], v)
        p = tuple(x + (y - x) * e for x, y in zip(a, p))
    q = (p[0] + p[2] / 2, p[1] + p[3] / 2, p[2])
    if prev:
        d = abs(q[0] - prev[0]) + abs(q[1] - prev[1]) + abs(q[2] - prev[2])
        if d > worst[0]:
            worst = (d, v)
    prev = q
print(f"worst window change: {worst[0]:.1f} px/frame at {worst[1]:.2f}s  (smooth glides peak ~30; a lone spike = a jump)")
for sg in r.SEGMENTS:
    sp = [r.speed(sg, v) for v in np.arange(sg["v0"], sg["v1"], 1 / r.FPS)]
    print(f"{sg['caption'][0][:28]:28} speed {min(sp):.2f}–{max(sp):.2f}x")
