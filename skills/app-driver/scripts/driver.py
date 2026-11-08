import json, math, os, subprocess, sys, tempfile, time

import shlex, shutil

S = os.environ["WORK"]  # work dir: home/, rec/, shots/, ctl, driver.log
HERE = os.path.dirname(os.path.abspath(__file__))
CAGE = os.environ.get("CAGE") or shutil.which("cage")
GRIM = os.environ.get("GRIM") or shutil.which("grim")
RANDR = os.environ.get("WLR_RANDR") or shutil.which("wlr-randr")
WFREC = os.environ.get("WF_RECORDER") or shutil.which("wf-recorder")
VPTR = f"{HERE}/vptr/target/release/vptr"
APP = shlex.split(os.environ["APP"])  # the GUI command, e.g. "/path/to/target/release/riven"
CTL = f"{S}/ctl"
MODE = os.environ.get("MODE", "2560x1440")
SCALE = os.environ.get("SCALE", "2")

env = dict(os.environ)
env.pop("DISPLAY", None)
env.update(
    XDG_DATA_HOME=f"{S}/home/data",
    XDG_CONFIG_HOME=f"{S}/home/config",
    XDG_RUNTIME_DIR=tempfile.mkdtemp(),
    WLR_BACKENDS="headless",
    WLR_LIBINPUT_NO_DEVICES="1",
    WLR_HEADLESS_OUTPUTS="1",
)
log = open(f"{S}/driver.log", "a")
cage = subprocess.Popen([CAGE, "-s", "--", *APP], env=env, stdout=open(f"{S}/cage.log", "w"), stderr=subprocess.STDOUT)
for _ in range(100):
    ws = [w for w in os.listdir(env["XDG_RUNTIME_DIR"]) if w.startswith("wayland-") and not w.endswith(".lock")]
    if ws:
        break
    time.sleep(0.1)
env["WAYLAND_DISPLAY"] = ws[0]
time.sleep(0.5)
subprocess.run([RANDR, "--output", "HEADLESS-1", "--custom-mode", f"{MODE}@60Hz", "--scale", SCALE], env=env, stdout=log, stderr=log)
env["VPTR_SIZE"] = os.environ.get("LOGICAL", "1280x720")
vp = subprocess.Popen([VPTR], env=env, stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True, bufsize=1)

pos = [640.0, 360.0]
rec = None
t0 = None
events = None


def ev(kind, **kw):
    if events:
        events.write(json.dumps({"t": round(time.monotonic() - t0, 4), "e": kind, **kw}) + "\n")
        events.flush()


def send(cmd):
    vp.stdin.write(cmd + "\n")
    vp.stdout.readline()


def move(x, y, dur):
    sx, sy = pos
    dist = math.hypot(x - sx, y - sy)
    if dur is None:
        dur = min(0.9, 0.25 + dist / 1400)
    n = max(1, int(dur * 120))
    # slight arc so the path doesn't look robotic
    nx, ny = -(y - sy), (x - sx)
    bend = 0.08 * (1 if (int(sx + sy) % 2) else -1)
    start = time.monotonic()
    for i in range(1, n + 1):
        u = i / n
        e = u * u * u * (u * (6 * u - 15) + 10)
        a = math.sin(math.pi * e) * bend
        px, py = sx + (x - sx) * e + nx * a, sy + (y - sy) * e + ny * a
        send(f"move {px:.2f} {py:.2f}")
        ev("move", x=round(px, 2), y=round(py, 2))
        wait = start + i / 120 - time.monotonic()
        if wait > 0:
            time.sleep(wait)
    pos[:] = [x, y]


def start_rec(path):
    return subprocess.Popen([WFREC, "-y", "-r", "60", "-c", "libx264", "-p", "crf=12", "-p", "preset=ultrafast", "-f", path],
                            env=env, stdout=log, stderr=log)


def stop_rec(r):
    r.send_signal(2)
    try:
        r.wait(timeout=8)
    except subprocess.TimeoutExpired:
        r.kill()


def handle(line):
    global rec, t0, events
    p = line.split()
    if not p:
        return
    c = p[0]
    if c == "move":
        move(float(p[1]), float(p[2]), float(p[3]) if len(p) > 3 else None)
    elif c in ("click", "rclick"):
        if len(p) > 2:
            move(float(p[1]), float(p[2]), float(p[3]) if len(p) > 3 else None)
            time.sleep(0.08)
        ev(c, x=pos[0], y=pos[1])
        send(c)
    elif c in ("down", "up"):
        if len(p) > 2:
            move(float(p[1]), float(p[2]), float(p[3]) if len(p) > 3 else None)
        ev(c, x=pos[0], y=pos[1])
        send(c)
    elif c == "scroll":
        for _ in range(abs(int(p[1]))):
            ev("scroll", d=int(p[1]))
            send(f"scroll {1 if int(p[1]) > 0 else -1}")
            time.sleep(float(p[2]) if len(p) > 2 else 0.06)
    elif c == "key":
        ev("key", k=p[1])
        send(line)
    elif c == "type":
        text = line[5:]
        for ch in text:
            ev("type", ch=ch)
            send(f"type {ch}")
            time.sleep(0.07)
    elif c == "mark":
        ev("mark", name=" ".join(p[1:]))
    elif c == "sleep":
        time.sleep(float(p[1]))
    elif c == "at":
        # wait until T seconds after `rec start` — lets a take run on an exact timeline
        wait = t0 + float(p[1]) - time.monotonic()
        if wait > 0:
            time.sleep(wait)
        elif wait < -0.03:
            print(f"late by {-wait:.2f}s at {p[1]}", file=log, flush=True)
    elif c == "shot":
        subprocess.run([GRIM, f"{S}/shots/{p[1]}.png"], env=env)
    elif c == "rec":
        if p[1] == "start":
            out = p[2]
            rec = start_rec(out)
            t0 = time.monotonic()
            events = open(out.rsplit(".", 1)[0] + ".events.jsonl", "w")
            ev("start", x=pos[0], y=pos[1])
        else:
            ev("stop")
            stop_rec(rec)
            events.close()
            events = None
    elif c == "quit":
        raise SystemExit


os.makedirs(f"{S}/shots", exist_ok=True)
if not os.path.exists(CTL):
    os.mkfifo(CTL)
print("ready", env["WAYLAND_DISPLAY"], file=log, flush=True)
try:
    while True:
        with open(CTL) as f:
            for line in f:
                print(">", line.strip(), file=log, flush=True)
                handle(line.strip())
                print("done", file=log, flush=True)
finally:
    if rec:
        rec.send_signal(2)
        rec.wait()
    vp.kill()
    cage.terminate()
    cage.wait()
