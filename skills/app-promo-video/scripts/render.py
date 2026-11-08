import json, math, os, subprocess, sys
from multiprocessing import Pool

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageChops

S = os.environ["WORK"]
FF = os.environ.get("FFMPEG", "ffmpeg")
# one or more takes, comma-separated: a scene names its take by index (take_seg(..., take=k))
TAKES = os.environ.get("TAKE", "take").split(",")
RAWS = [f"{S}/rec/{t}.mp4" for t in TAKES]
EVENTS = [f"{S}/rec/{t}.events.jsonl" for t in TAKES]
MUSIC = os.environ.get("MUSIC", f"{S}/music.wav")
LOGO = os.environ["LOGO"]  # square RGBA png
FONT = os.environ["FONT"]  # Inter variable ttf
NERD_FONT = os.environ["NERD_FONT"]  # any Nerd Font ttf (GitHub glyph U+F09B)
CACHES = [f"{S}/cache/{t}" for t in TAKES]
OUT = sys.argv[1] if len(sys.argv) > 1 else f"{S}/teaser.mp4"
PREVIEW = os.environ.get("PREVIEW")  # comma-separated times → PNGs instead of a video

W, H, FPS = 1920, 1080, 60
SW, SH = 2560, 1440  # raw recording
LS = 2.0  # raw pixels per logical pixel
BEAT = 60 / 128
BAR = 4 * BEAT
BARS = int(os.environ.get("BARS", "24"))
TOTAL = BARS * BAR

ACCENT = (110, 168, 254)
TEXT = (240, 244, 252)
MUTED = (160, 174, 200)

# Each segment plays the raw recording between video times v0..v1, warped so that
# every anchor (raw event time -> video time) lands on the beat.
B = lambda n: n * BEAT  # beat n of the song


def seg(v0, v1, anchors, s0=1.0, s1=1.0, cam=(), caption=None):
    return dict(v0=v0, v1=v1, anchors=anchors, s0=s0, s1=s1, cam=cam, caption=caption)


# One real-time take recorded on the video's timeline by schedule.py (see reference/riven-schedule.txt and the PLAN file):
# event time E0 + (beat - 8) * BEAT happens at video beat `beat`, so every segment plays the take 1:1 and the
# segments only switch captions. E0 must match the schedule's pre-roll.
E0 = float(os.environ.get("E0", "4.0"))


def take_seg(b0, b1, cam, caption, hold=None, take=0, first=8, skip_label=None):
    """A scene of take `take` (scheduled from beat `first`) played 1:1; `hold` = event time to freeze on.

    A long wait (a cold modpack install) is never recorded: the take stops before it, the next take starts from
    the finished state, and its first scene sets `skip_label` — a dissolve under a "… later" pill.
    """
    anchors = [(E0 + (b0 - first) * BEAT, B(b0))]
    if hold is not None:
        anchors.append((hold, B(b0) + hold - anchors[0][0]))
    sg = seg(B(b0), B(b1), anchors, s1=0.0 if hold is not None else 1.0, cam=cam, caption=caption)
    sg["skip_label"] = skip_label
    sg["take"] = take
    return sg


PLAN = os.environ.get("PLAN", os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "reference", "riven-plan.py"))
exec(compile(open(PLAN).read(), PLAN, "exec"))
CONTINUOUS = {sg["v0"] for sg in SEGMENTS[1:] if not sg.get("skip_label")}  # one take; cuts only at skips
XFADE = 0.8
INTRO_END, OUTRO_START = 2 * BAR, (BARS - 2) * BAR


def warp(sg, v):
    a = sg["anchors"]
    if v <= a[0][1]:
        return a[0][0] - (a[0][1] - v) * sg["s0"]
    for (r0, t0), (r1, t1) in zip(a, a[1:]):
        if v <= t1:
            return r0 + (v - t0) * (r1 - r0) / (t1 - t0)
    return a[-1][0] + (v - a[-1][1]) * sg["s1"]


def speed(sg, v):
    return (warp(sg, v + 0.01) - warp(sg, v - 0.01)) / 0.02


def seg_at(v):
    for sg in SEGMENTS:
        if sg["v0"] <= v < sg["v1"]:
            return sg
    return None


def raw_frame(sg, rt):
    return sg.get("take", 0), max(0, int(round((rt - REC_LAGS[sg.get("take", 0)]) * FPS)))


def frame_plan():
    """For every output frame: (segment index or None, raw frame index or None)."""
    plan = []
    for i in range(int(TOTAL * FPS)):
        v = i / FPS
        sg = seg_at(v)
        if sg:
            plan.append((SEGMENTS.index(sg), raw_frame(sg, warp(sg, v))))
        else:
            plan.append((None, None))
    return plan


def needed_frames():
    idx = set()
    for _, r in frame_plan():
        if r is not None:
            idx.add(r)
    # the last frame of each segment is also used for transitions
    for sg in SEGMENTS:
        for f in range(int(XFADE * FPS) + 2):
            idx.add(raw_frame(sg, warp(sg, sg["v1"] + f / FPS)))
        idx.add(raw_frame(sg, warp(sg, sg["v1"] - 1e-3)))
        idx.add(raw_frame(sg, warp(sg, sg["v0"])))
    return sorted(idx)


def extract():
    for k, (raw, cache) in enumerate(zip(RAWS, CACHES)):
        os.makedirs(cache, exist_ok=True)
        need = [i for t, i in needed_frames() if t == k and not os.path.exists(f"{cache}/{i:05d}.jpg")]
        if not need:
            continue
        want = set(need)
        last = max(need)
        p = subprocess.Popen([FF, "-v", "error", "-i", raw, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE, bufsize=SW * SH * 3)
        n = 0
        size = SW * SH * 3
        while n <= last:
            buf = p.stdout.read(size)
            if len(buf) < size:
                break
            if n in want:
                Image.frombuffer("RGB", (SW, SH), buf, "raw", "RGB", 0, 1).save(f"{cache}/{n:05d}.jpg", quality=95, subsampling=0)
            n += 1
        p.kill()
        print("extracted", len(need), "frames from", TAKES[k], file=sys.stderr)


def load_raw(ref):
    k, i = ref
    path = f"{CACHES[k]}/{i:05d}.jpg"
    while not os.path.exists(path) and i > 0:
        i -= 1
        path = f"{CACHES[k]}/{i:05d}.jpg"
    return Image.open(path).convert("RGB")


# ---------------------------------------------------------------- helpers
def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def ease(t):
    t = clamp(t)
    return t * t * (3 - 2 * t)


def ease_out(t, p=3):
    t = clamp(t)
    return 1 - (1 - t) ** p


def ease_back(t, c=1.6):
    t = clamp(t)
    return 1 + (c + 1) * (t - 1) ** 3 + c * (t - 1) ** 2


def font(size, weight="Bold"):
    f = ImageFont.truetype(FONT, size)
    f.set_variation_by_name(weight)
    return f


EVENTS_LISTS = [[json.loads(l) for l in open(e)] for e in EVENTS]


def _rec_lag(raw, events):
    """Event clock minus recording clock, found by lining up on-screen motion with the logged inputs.

    wf-recorder starts 0.05–2.5 s after `rec start` and may lose its tail when it hangs on exit, so neither
    end of the file can be trusted; the cursor can.
    """
    cache = raw + ".lag"
    if os.path.exists(cache) and os.path.getmtime(cache) > os.path.getmtime(raw):
        return float(open(cache).read())
    w, h = 320, 180
    p = subprocess.run([FF, "-v", "error", "-i", raw, "-vf", f"scale={w}:{h},format=gray", "-f", "rawvideo", "-"],
                       capture_output=True).stdout
    frames = np.frombuffer(p, np.uint8).reshape(-1, h, w).astype(np.int16)
    vid = (np.abs(np.diff(frames, axis=0)) > 6).sum(axis=(1, 2)) > 0  # frame i+1 differs from frame i
    n = len(vid) + 1
    span = int((events[-1]["t"] + 1) * FPS)
    ev = np.zeros(span, bool)
    for e in events:
        if e["e"] in ("move", "click", "scroll", "type", "down", "up"):
            ev[min(span - 1, int(e["t"] * FPS))] = True
    best = (-1e9, 0)
    pad = int(FPS)  # rendering latency can put the frame showing an input after it (negative lag)
    ev = np.concatenate([np.zeros(pad, bool), ev])
    for lag in range(-pad, int(4 * FPS)):
        a = ev[pad + lag + 1 : pad + lag + n]  # event bins that land on video frames 1..n-1
        k = min(len(a), len(vid))
        score = np.sum(a[:k] & vid[:k]) - 0.5 * np.sum(a[:k] & ~vid[:k]) - 0.5 * np.sum(~a[:k] & vid[:k])
        if score > best[0]:
            best = (score, lag)
    lag = best[1] / FPS
    open(cache, "w").write(f"{lag:.4f}")
    return lag


REC_LAGS = [_rec_lag(r, e) for r, e in zip(RAWS, EVENTS_LISTS)]


def _key(e):
    return (e["e"], e.get("ch"), e.get("x") if e["e"] != "scroll" else None, e.get("name"))


def _remapper():
    """The edit plan's raw times refer to REF_EVENTS' take; map them onto this take by matching its events."""
    ref = os.environ.get("REF_EVENTS")
    if not ref or len(TAKES) > 1 or os.path.abspath(ref) == os.path.abspath(EVENTS[0]):
        return lambda t: t
    old = [json.loads(l) for l in open(ref)]
    old = [e for e in old if e["e"] not in ("move", "stop")]
    new = [e for e in EVENTS_LISTS[0] if e["e"] not in ("move", "stop")]
    if [_key(e) for e in old] != [_key(e) for e in new]:
        sys.exit("REF_EVENTS and this take differ in their events; anchors must be rewritten by hand")
    ot, nt = np.array([e["t"] for e in old]), np.array([e["t"] for e in new])
    return lambda t: float(np.interp(t, ot, nt)) if ot[0] <= t <= ot[-1] else t + (nt[0] - ot[0] if t < ot[0] else nt[-1] - ot[-1])


REMAP = _remapper()
for _sg in SEGMENTS:
    _sg["anchors"] = [(REMAP(r), v) for r, v in _sg["anchors"]]
CLICKS = [[e for e in ev if e["e"] in ("click", "down")] for ev in EVENTS_LISTS]

def _cam_target(keys, v):
    if v <= keys[0][0]:
        return keys[0][1:]
    for a, b in zip(keys, keys[1:]):
        if v <= b[0]:
            u = (v - a[0]) / (b[0] - a[0])
            return tuple(a[i] + (b[i] - a[i]) * u for i in (1, 2, 3))
    return keys[-1][1:]


def _smooth_track(sg, sigma=0.45):
    """Camera path for a segment (plus the dissolve tail): linear between keys, then Gaussian-smoothed."""
    pad = int(sigma * 3 * FPS)
    n0, n1 = int(round(sg["v0"] * FPS)), int(round((sg["v1"] + XFADE) * FPS)) + 1
    vs = np.arange(n0 - pad, n1 + pad) / FPS
    tgt = np.array([_cam_target(sg["cam"], v) for v in vs], np.float64)
    tgt[:, 2] = np.log(tgt[:, 2])  # zoom is smoothed in log space so it feels even
    k = np.arange(-pad, pad + 1) / FPS
    ker = np.exp(-0.5 * (k / sigma) ** 2)
    ker /= ker.sum()
    out = np.stack([np.convolve(np.pad(tgt[:, c], pad, mode="edge"), ker, mode="same")[pad:-pad] for c in range(3)], 1)
    out[:, 2] = np.exp(out[:, 2])
    return n0 - pad, out


def _tracks():
    """One smoothed path per run of segments joined without a cut."""
    tracks, run = {}, []
    for sg in SEGMENTS + [None]:
        if run and (sg is None or sg["v0"] not in CONTINUOUS):
            keys = sorted({k for r in run for k in r["cam"]})
            merged = dict(run[0], v1=run[-1]["v1"], cam=keys)
            tr = _smooth_track(merged)
            for r in run:
                tracks[id(r)] = tr
            run = []
        if sg is not None:
            run.append(sg)
    return tracks


TRACKS = _tracks()


def camera(sg, v):
    start, arr = TRACKS[id(sg)]
    i = min(len(arr) - 1, max(0, int(round(v * FPS)) - start))
    return tuple(arr[i])


# ---------------------------------------------------------------- background
_yy, _xx = np.mgrid[0:270, 0:480].astype(np.float32)


def background(v):
    t = v
    base = np.zeros((270, 480, 3), np.float32)
    base[:] = (7, 10, 22)
    blobs = [
        ((0.25 + 0.08 * math.sin(t * 0.5), 0.3 + 0.06 * math.cos(t * 0.4)), 170, (40, 80, 190), 0.9),
        ((0.78 + 0.07 * math.cos(t * 0.35), 0.72 + 0.08 * math.sin(t * 0.45)), 200, (70, 50, 170), 0.7),
        ((0.6 + 0.1 * math.sin(t * 0.3 + 1), 0.15 + 0.05 * math.sin(t * 0.6)), 140, (30, 120, 200), 0.5),
    ]
    for (cx, cy), r, col, a in blobs:
        d2 = ((_xx - cx * 480) ** 2 + (_yy - cy * 270) ** 2) / (r * r)
        g = np.exp(-d2 * 2.2)[..., None] * a
        base += g * np.array(col, np.float32)
    # faint moving tide lines
    for i in range(5):
        y0 = 270 * (0.68 + i * 0.06)
        yy = y0 + (6 + 2 * i) * np.sin(_xx / (60 + 9 * i) + t * (0.6 + 0.1 * i) * (1 if i % 2 else -1) + i)
        line = np.exp(-((_yy - yy) ** 2) / 0.9)[..., None] * (26 - 4 * i)
        base += line * np.array((90, 140, 255), np.float32) / 255
    img = Image.fromarray(np.clip(base, 0, 255).astype(np.uint8)).resize((W, H), Image.BILINEAR)
    return img


# ---------------------------------------------------------------- window compositing
RADIUS = 22


def _fit(pos, size, full, margin=40):
    m = margin * clamp((full + 200 - size) / (2 * margin + 200))  # margin fades out as the window outgrows the frame
    lo, hi = full - m - size, m
    if lo >= hi:
        return (full - size) / 2
    return clamp(pos, lo, hi)


def place(sg, v):
    """Window rectangle on screen (x, y, w, h) and the logical->screen mapping."""
    cx, cy, z = camera(sg, v) if sg else (640, 360, 1.0)
    scale = 1500 / 1280 * z  # screen px per logical px
    ww, wh = 1280 * scale, 720 * scale
    x = _fit(W / 2 - cx * scale, ww, W)
    y = _fit(H / 2 - cy * scale + 10, wh, H)
    return x, y, ww, wh, scale


def draw_window(canvas, raw, x, y, ww, wh, alpha=1.0, shadow=True):
    x0, y0 = max(0, int(math.floor(x))), max(0, int(math.floor(y)))
    x1, y1 = min(W, int(math.ceil(x + ww))), min(H, int(math.ceil(y + wh)))
    if x1 <= x0 or y1 <= y0:
        return
    if shadow:
        sh = Image.new("L", (W // 8, H // 8), 0)
        ImageDraw.Draw(sh).rounded_rectangle([(x + 6) / 8, (y + 26) / 8, (x + ww - 6) / 8, (y + wh + 30) / 8], RADIUS / 8, fill=int(200 * alpha))
        sh = sh.filter(ImageFilter.GaussianBlur(6)).resize((W, H), Image.BILINEAR)
        canvas.paste((0, 0, 0), (0, 0), sh)
        glow = Image.new("L", (W // 8, H // 8), 0)
        ImageDraw.Draw(glow).rounded_rectangle([x / 8, y / 8, (x + ww) / 8, (y + wh) / 8], RADIUS / 8, fill=int(70 * alpha))
        glow = glow.filter(ImageFilter.GaussianBlur(10)).resize((W, H), Image.BILINEAR)
        canvas.paste(ACCENT, (0, 0), glow)
    sx = SW / ww
    sy = SH / wh
    box = (max(0.0, (x0 - x) * sx), max(0.0, (y0 - y) * sy), min(SW, (x1 - x) * sx), min(SH, (y1 - y) * sy))
    part = raw.resize((x1 - x0, y1 - y0), Image.BICUBIC, box=box, reducing_gap=2.0)
    mask = Image.new("L", (x1 - x0, y1 - y0), 0)
    ImageDraw.Draw(mask).rounded_rectangle([x - x0, y - y0, x + ww - x0 - 1, y + wh - y0 - 1], RADIUS * ww / 1500, fill=int(255 * alpha))
    canvas.paste(part, (x0, y0), mask)
    border = Image.new("L", (x1 - x0, y1 - y0), 0)
    ImageDraw.Draw(border).rounded_rectangle([x - x0, y - y0, x + ww - x0 - 1, y + wh - y0 - 1], RADIUS * ww / 1500, outline=int(70 * alpha), width=2)
    canvas.paste((150, 180, 255), (x0, y0), border)


def draw_clicks(ov, sg, v, x, y, scale):
    d = ImageDraw.Draw(ov)
    for c in CLICKS[sg.get("take", 0)]:
        # find the video time of this click inside the segment
        rt = c["t"]
        lo, hi = sg["v0"] - 0.5, sg["v1"]
        if not (warp(sg, lo) <= rt <= warp(sg, hi)):
            continue
        for _ in range(40):
            mid = (lo + hi) / 2
            if warp(sg, mid) < rt:
                lo = mid
            else:
                hi = mid
        tv = hi
        age = v - tv
        if not (0 <= age < 0.45) or tv < sg["v0"]:
            continue
        u = age / 0.45
        px, py = x + c["x"] * scale, y + c["y"] * scale
        r = 14 + 46 * ease_out(u)
        al = int(230 * (1 - u) ** 1.5)
        d.ellipse([px - r, py - r, px + r, py + r], outline=ACCENT + (al,), width=max(2, int(5 * (1 - u)) + 1))
        r2 = 22 * (1 - ease_out(u * 1.6)) + 2
        if u < 0.5:
            d.ellipse([px - r2, py - r2, px + r2, py + r2], fill=(255, 255, 255, int(110 * (1 - u * 2))))


# ---------------------------------------------------------------- text
F_TITLE = font(64, "ExtraBold")
F_SUB = font(30, "Medium")
F_BIG = font(120, "ExtraBold")
F_TAG = font(38, "Medium")
F_PILL = font(30, "Bold")
F_SPEED = font(26, "Bold")
F_GH = font(36, "SemiBold")
F_GH_ICON = ImageFont.truetype(NERD_FONT, 44)
GH_ICON = "\uf09b"


def text_layer():
    return Image.new("RGBA", (W, H), (0, 0, 0, 0))


def draw_caption(ov, caption, age, out_age=None):
    title, sub = caption
    d = ImageDraw.Draw(ov)
    k = ease_out(age / 0.35)
    fade = 1.0 if out_age is None else 1 - ease(out_age / 0.18)
    if k <= 0 or fade <= 0:
        return
    x = 96
    y = H - 210 + (1 - k) * 40
    # backing gradient for legibility
    g = Image.new("L", (1, 360))
    for i in range(360):
        g.putpixel((0, i), int(210 * (i / 359) ** 1.6 * fade))
    g = g.resize((W, 360))
    ov.paste((4, 6, 14, 255), (0, H - 360), g)
    d = ImageDraw.Draw(ov)
    bar_h = 86 * k
    d.rounded_rectangle([x - 26, y + 6, x - 18, y + 6 + bar_h], 4, fill=ACCENT + (int(255 * fade),))
    words = title.split(" ")
    cx = x
    for i, w in enumerate(words):
        wk = ease_out((age - i * 0.05) / 0.3)
        a = int(255 * wk * fade)
        d.text((cx, y + (1 - wk) * 30), w, font=F_TITLE, fill=TEXT + (a,))
        cx += d.textlength(w + " ", font=F_TITLE)
    sk = ease_out((age - 0.15) / 0.35)
    d.text((x, y + 82 + (1 - sk) * 20), sub, font=F_SUB, fill=MUTED + (int(255 * sk * fade),))


def draw_speed_badge(ov, s, v):
    if s < 2.4:
        return
    d = ImageDraw.Draw(ov)
    label = f"×{s:.0f}"
    tw = d.textlength(label, font=F_SPEED)
    x1, y0 = W - 70, 60
    d.rounded_rectangle([x1 - tw - 70, y0, x1, y0 + 52], 26, fill=(10, 14, 28, 200), outline=ACCENT + (180,), width=2)
    # fast-forward chevrons
    cx = x1 - tw - 46
    for k in range(2):
        px = cx + k * 14
        d.polygon([(px, y0 + 16), (px + 12, y0 + 26), (px, y0 + 36)], fill=ACCENT + (255,))
    d.text((x1 - tw - 18, y0 + 11), label, font=F_SPEED, fill=TEXT + (255,))


LOGO_IMG = Image.open(LOGO).convert("RGBA")


def logo(size, alpha=1.0, glow=0.0):
    im = LOGO_IMG.resize((size, size), Image.LANCZOS)
    if alpha < 1:
        a = im.getchannel("A").point(lambda p: int(p * alpha))
        im.putalpha(a)
    return im


def paste_center(canvas, im, cx, cy):
    canvas.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2)))


def glow_disc(canvas, cx, cy, r, color, alpha):
    g = Image.new("L", (W // 4, H // 4), 0)
    ImageDraw.Draw(g).ellipse([(cx - r) / 4, (cy - r) / 4, (cx + r) / 4, (cy + r) / 4], fill=int(255 * alpha))
    g = g.filter(ImageFilter.GaussianBlur(r / 10)).resize((W, H), Image.BILINEAR)
    canvas.paste(color, (0, 0), g)


def centered_text(d, cx, y, text, f, fill):
    tw = d.textlength(text, font=f)
    d.text((cx - tw / 2, y), text, font=f, fill=fill)
    return tw


# ---------------------------------------------------------------- scenes
def intro(v):
    canvas = background(v)
    first = SEGMENTS[0]
    raw = load_raw(raw_frame(first, warp(first, first["v0"])))
    k = clamp(v / INTRO_END)
    m = ease((v - (INTRO_END - 1.2)) / 1.2)  # morph into the first scene
    rx, ry, rw, rh, _ = place(first, first["v0"])
    s = 0.62 + 0.2 * ease(k)
    gw, gh = 1500 * s, 843.75 * s
    gx, gy = (W - gw) / 2, (H - gh) / 2 + 30
    x, y, ww, wh = (gx + (rx - gx) * m, gy + (ry - gy) * m, gw + (rw - gw) * m, gh + (rh - gh) * m)
    ghost = canvas.copy()
    draw_window(ghost, raw, x, y, ww, wh)
    radius = (14 - 6 * k) * (1 - m)
    if radius > 0.3:
        ghost = ghost.filter(ImageFilter.GaussianBlur(radius))
    canvas = Image.blend(canvas, ghost, 0.35 + 0.25 * k + 0.4 * m).convert("RGBA")
    canvas.alpha_composite(Image.new("RGBA", (W, H), (4, 6, 14, int(120 * (1 - 0.5 * k) * (1 - m)))))

    fade = 1 - ease((v - (INTRO_END - 1.2)) / 0.5)
    lift = -60 * m
    ov = text_layer()
    d = ImageDraw.Draw(ov)
    lk = ease_back((v - 0.15) / 0.7)
    if v > 0.15 and fade > 0:
        glow_disc(canvas, W / 2, 400 + lift, 220 + 30 * math.sin(v * 2), (60, 110, 230), clamp((v - 0.15) / 0.8) * 0.55 * fade)
        size = int(220 * (0.6 + 0.4 * lk))
        paste_center(canvas, logo(size, clamp((v - 0.15) / 0.3) * fade), W / 2, 400 + lift)
    if v > 0.8:
        title = TITLE
        cx = W / 2 - d.textlength(title, font=F_BIG) / 2
        for i, ch in enumerate(title):
            ck = ease_out((v - 0.8 - i * 0.03) / 0.35)
            d.text((cx, 560 + (1 - ck) * 50 + lift), ch, font=F_BIG, fill=TEXT + (int(255 * ck * fade),))
            cx += d.textlength(ch, font=F_BIG)
    if v > BAR:
        k2 = ease_out((v - BAR) / 0.5)
        centered_text(d, W / 2, 720 + (1 - k2) * 24 + lift, TAGLINE, F_TAG, MUTED + (int(255 * k2 * fade),))
    canvas.alpha_composite(ov)
    return canvas.convert("RGB")


def draw_skip_label(ov, v):
    """A dimmed screen and a "… later" pill around each labelled skip, so the cut reads as an honest time jump."""
    for s in SEGMENTS:
        label = s.get("skip_label")
        dt = v - s["v0"]
        if not label or not -0.8 < dt < 2.0:
            continue
        a = ease((dt + 0.8) / 0.5) * (1 - ease((dt - 1.4) / 0.6))
        if a <= 0:
            continue
        ov.alpha_composite(Image.new("RGBA", (W, H), (4, 6, 14, int(130 * a))))
        d = ImageDraw.Draw(ov)
        tw = d.textlength(label, font=F_TAG)
        icon = 46
        pw, ph = tw + icon + 96, 84
        cx, cy = W / 2, 200
        sc = 0.92 + 0.08 * ease_out((dt + 0.8) / 0.5)
        x0, y0 = cx - pw / 2 * sc, cy - ph / 2 * sc
        d.rounded_rectangle([x0, y0, cx + pw / 2 * sc, cy + ph / 2 * sc], ph / 2 * sc, fill=(10, 14, 28, int(235 * a)),
                            outline=ACCENT + (int(200 * a),), width=2)
        ix, iy = x0 + 40 * sc, cy
        for k in range(2):
            ox = ix + k * 20 * sc
            d.polygon([(ox, iy - 13 * sc), (ox + 20 * sc, iy), (ox, iy + 13 * sc)], fill=ACCENT + (int(255 * a),))
        d.text((ix + icon + 18 * sc, cy - 24), label, font=F_TAG, fill=TEXT + (int(255 * a),))


def app_frame(v, sg, raw, placement=None):
    canvas = background(v)
    x, y, ww, wh, scale = placement or place(sg, v)
    draw_window(canvas, raw, x, y, ww, wh)
    ov = text_layer()
    draw_skip_label(ov, v)
    draw_clicks(ov, sg, v, x, y, scale)
    s = speed(sg, v)
    if s >= 2.4:
        draw_speed_badge(ov, s, v)
    # caption: shown for the whole run of segments that share it
    cap = sg["caption"]
    start = sg["v0"]
    i = SEGMENTS.index(sg)
    while i > 0 and SEGMENTS[i - 1]["caption"] == cap and SEGMENTS[i - 1]["v1"] == start:
        i -= 1
        start = SEGMENTS[i]["v0"]
    end = sg["v1"]
    j = SEGMENTS.index(sg)
    while j + 1 < len(SEGMENTS) and SEGMENTS[j + 1]["caption"] == cap and SEGMENTS[j + 1]["v0"] == end:
        j += 1
        end = SEGMENTS[j]["v1"]
    out_age = v - (end - 0.18) if v > end - 0.18 else None
    draw_caption(ov, cap, v - start - 0.05, out_age)
    canvas = canvas.convert("RGBA")
    canvas.alpha_composite(ov)
    return canvas.convert("RGB")


def outro(v):
    t = v - OUTRO_START
    canvas = background(v).convert("RGBA")
    last = SEGMENTS[-1]
    raw = load_raw(raw_frame(last, warp(last, last["v1"] - 1e-3)))
    k = ease_out(t / 0.7, 4)
    if t < 1.2:
        x, y, ww, wh, _ = place(last, last["v1"] - 1e-3)
        z = 1 - k * 0.72
        cx, cy = x + ww / 2, y + wh / 2
        nw, nh = ww * z, wh * z
        ncx, ncy = cx + (W / 2 - cx) * k, cy + (H / 2 + 260 - cy) * k
        layer = Image.new("RGB", (W, H))
        layer.paste(canvas.convert("RGB"))
        draw_window(layer, raw, ncx - nw / 2, ncy - nh / 2, nw, nh)
        a = 1 - clamp((t - 0.5) / 0.6)
        canvas = Image.blend(canvas.convert("RGB"), layer, a).convert("RGBA")
    ov = text_layer()
    d = ImageDraw.Draw(ov)
    lk = ease_back((t - 0.1) / 0.6)
    glow_disc(canvas, W / 2, 360, 260 + 20 * math.sin(t * 5), (60, 110, 230), 0.6 * clamp(t / 0.4))
    if t > 0.1:
        paste_center(canvas, logo(int(230 * (0.5 + 0.5 * lk)), clamp((t - 0.1) / 0.25)), W / 2, 360)
    if t > 0.35:
        tk = ease_out((t - 0.35) / 0.5)
        centered_text(d, W / 2, 520 + (1 - tk) * 40, TITLE, F_BIG, TEXT + (int(255 * tk),))
    if t > 0.9:
        gk = ease_out((t - 0.9) / 0.5)
        a = int(255 * gk)
        label = LINK
        gw = d.textlength(GH_ICON, font=F_GH_ICON) + 26 + d.textlength(label, font=F_GH)
        gx = W / 2 - gw / 2
        gy = 690 + (1 - gk) * 20
        d.text((gx, gy - 2), GH_ICON, font=F_GH_ICON, fill=TEXT + (a,))
        d.text((gx + d.textlength(GH_ICON, font=F_GH_ICON) + 26, gy), label, font=F_GH, fill=TEXT + (a,))
    canvas.alpha_composite(ov)
    fade = clamp((TOTAL - v - 0.05) / 0.7)
    if fade < 1:
        canvas.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, int(255 * (1 - fade)))))
    return canvas.convert("RGB")


def scene_raw(v, sg):
    return load_raw(raw_frame(sg, warp(sg, v)))


def render(i):
    v = i / FPS
    if v < INTRO_END:
        img = intro(v)
    elif v >= OUTRO_START:
        img = outro(v)
    else:
        sg = seg_at(v)
        raw = scene_raw(v, sg)
        placement = None
        k = SEGMENTS.index(sg)
        if k > 0 and sg["v0"] not in CONTINUOUS and v - sg["v0"] < XFADE:
            # one window: content dissolves while the camera glides from the old framing to the new one
            prev = SEGMENTS[k - 1]
            e = ease((v - sg["v0"]) / XFADE)
            raw = Image.blend(scene_raw(v, prev), raw, e)
            a, b = place(prev, v), place(sg, v)
            placement = tuple(p + (q - p) * e for p, q in zip(a, b))
        img = app_frame(v, sg, raw, placement)
    return img.tobytes()


def main():
    extract()
    if PREVIEW:
        os.makedirs(f"{S}/preview", exist_ok=True)
        for t in PREVIEW.split(","):
            i = int(float(t) * FPS)
            Image.frombytes("RGB", (W, H), render(i)).save(f"{S}/preview/p_{float(t):05.2f}.png")
        return
    n = int(TOTAL * FPS)
    enc = subprocess.Popen([FF, "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                            "-i", MUSIC, "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "slow", "-crf", "16",
                            "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "320k", "-shortest", "-movflags", "+faststart", OUT],
                           stdin=subprocess.PIPE)
    with Pool(11) as pool:
        for k, buf in enumerate(pool.imap(render, range(n), chunksize=4)):
            enc.stdin.write(buf)
            if k % 120 == 0:
                print(f"{k}/{n}", file=sys.stderr, flush=True)
    enc.stdin.close()
    enc.wait()


if __name__ == "__main__":
    main()
