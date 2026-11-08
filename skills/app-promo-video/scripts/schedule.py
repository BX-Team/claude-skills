"""Turns a beat-timed schedule into a driver take that runs on the video's exact timeline.

usage: schedule.py SCHEDULE > take.run

Schedule lines: `BEAT ACTION ARGS`, e.g.
    9     click 75 164        # the click lands on beat 9
    10.5  type vred           # first key on beat 10.5
    27    scroll 30 0.05      # 30 notches, 50 ms apart, starting on beat 27
    63    move 800 300        # the cursor arrives on beat 63
    77.8  down 422 547        # press on beat 77.8 …
    79.5  up 600 547          # … drag there and release on beat 79.5
    88    mark end
Video beat b happens at recording-event time E0 + (b - FIRST_BEAT) * BEAT, so render.py can map
the take 1:1 (no time warp). Lines starting with # are ignored.
"""
import os, sys

BEAT = 60 / float(os.environ.get("BPM", "128"))
FIRST_BEAT = float(os.environ.get("FIRST_BEAT", "8"))  # first beat of the app part (after the intro)
E0 = float(os.environ.get("E0", "4.0"))  # pre-roll: wf-recorder can take >2 s to start


def at(b):
    return E0 + (b - FIRST_BEAT) * BEAT


rows = []
for line in open(sys.argv[1]):
    line = line.split("#", 1)[0].strip()
    if line:
        b, rest = line.split(None, 1)
        rows.append((float(b), rest.split()))

work = os.environ["WORK"]
take = os.environ.get("TAKE", "take")
out = [f"rec start {work}/rec/{take}.mp4"]
free = 0.0  # when the previous action is over
for b, (cmd, *args) in rows:
    t = at(b)
    if cmd in ("click", "rclick", "down", "move"):
        dur = max(0.2, min(0.7, (t - free) * 0.8))
        lead = dur + (0.08 if cmd != "move" else 0.0)
        out += [f"at {t - lead:.3f}", f"{cmd} {args[0]} {args[1]} {dur:.3f}"]
        free = t + 0.1
    elif cmd == "up":
        # drag: move from the press to here, arriving on the beat, then release
        dur = max(0.2, t - free)
        out += [f"at {t - dur:.3f}", f"move {args[0]} {args[1]} {dur:.3f}", "up"]
        free = t + 0.1
    elif cmd == "type":
        out += [f"at {t:.3f}", "type " + " ".join(args)]
        free = t + 0.11 * len(" ".join(args))
    elif cmd == "scroll":
        out += [f"at {t:.3f}", "scroll " + " ".join(args)]
        free = t + abs(int(args[0])) * (float(args[1]) if len(args) > 1 else 0.06) + 0.05
    else:
        out += [f"at {t:.3f}", " ".join([cmd, *args])]
        free = t
out += [f"at {free + 1.0:.3f}", "rec stop"]
print("\n".join(out))
