---
name: app-driver
description: Run a desktop GUI app (gpui, GTK, Qt, any Wayland client) in a headless compositor that never appears on the user's screen, and drive it yourself with real mouse moves, clicks, drags, scrolling, typing and screenshots. Use while developing a GUI app to try a change in the real app, reproduce or verify a UI bug, click through a flow, or take screenshots of it, instead of asking the user to do it. Also the recording layer under app-promo-video. Linux with Nix.
---

# Drive a GUI app off-screen

The app runs inside [cage](https://github.com/cage-kiosk/cage) on a headless wlroots output. A small Rust helper,
`vptr`, keeps one virtual pointer and one virtual keyboard alive in that session, and `driver.py` reads commands
from a FIFO, performs them with human-looking timing and logs each one. You look at the result with `shot`, then
open the PNG with your image-reading tool. Nothing shows up on the user's desktop, and the user's own data is
never touched.

```
scripts/
  tools.sh    eval "$(tools.sh)": nix-builds cage, grim, wlr-randr, wf-recorder, ffmpeg, a numpy/pillow/scipy Python, and vptr
  vptr/       virtual pointer + keyboard (zwlr_virtual_pointer_v1, zwp_virtual_keyboard_v1)
  driver.py   runs the app in cage, reads commands from $WORK/ctl, logs every event with a timestamp
  start.sh    (re)starts driver.py; `start.sh clean` first restores $WORK/home from $WORK/home.clean
  do.sh       do.sh 'cmd' 'cmd' …: sends commands and waits for each one to finish
  run.sh      run.sh FILE: sends every line of a file
```

`$SKILL` below is this skill's directory.

## 1. Setup

```bash
export WORK=<a scratch dir>          # home/, home.clean/, rec/, shots/, ctl and driver.log live here
export APP="/path/to/app --args"     # split like a shell command line
eval "$($SKILL/scripts/tools.sh)"     # first run builds everything through nix, later runs are instant
```

- **The app's data is sandboxed.** driver.py sets `XDG_DATA_HOME=$WORK/home/data` and
  `XDG_CONFIG_HOME=$WORK/home/config`. Seed only what the check needs; never point those at the user's real
  directories. Copied configs may hold absolute paths (recent projects, last folder): rewrite them to `$WORK/home/…`.
- When a check needs a known starting state, build it once and freeze it: `cp -a $WORK/home $WORK/home.clean`.
  `start.sh clean` then restores it before every run, so each attempt starts from the same place.
- Never copy tokens, keyrings or other secrets from the user's data without asking. Expect the app to behave as
  signed out.
- The app must find its own runtime libraries. For a Nix project, run `start.sh` inside its `nix develop`.
- Prefer a release build where the app is heavy: a debug gpui build is slow enough to change what you see.

## 2. Start, drive, look

```bash
nix develop -c $SKILL/scripts/start.sh clean     # or just start.sh, without nix develop or without a clean state
$SKILL/scripts/do.sh 'click 75 132' 'type hello' 'key 28' 'sleep 1' 'shot after-enter'
```

Then read `$WORK/shots/after-enter.png`. Commands (coordinates are LOGICAL pixels of a 1280×720 window):

| command | effect |
|---|---|
| `move X Y [DUR]` | eased move with a slight arc in 120 Hz steps (duration from the distance by default) |
| `click X Y [DUR]` / `rclick X Y [DUR]` | move there, then click; without X Y, click where the cursor is |
| `down X Y` · `move …` · `up` | drag: press, move, release (sliders, selections) |
| `scroll N [GAP]` | N wheel notches (+ is down), GAP seconds apart (default 0.06) |
| `type TEXT` | real key presses: a–z, A–Z, 0–9, space and `- . / : _` |
| `key CODE` | one evdev key code: 1 Esc, 14 Backspace, 15 Tab, 28 Enter, 103/108 Up/Down |
| `sleep S` / `mark NAME` | wait / put a named marker into the event log |
| `shot NAME` | screenshot to `$WORK/shots/NAME.png` |
| `rec start FILE.mp4` / `rec stop` | record at 60 fps with wf-recorder; events go to `FILE.events.jsonl` |
| `at T` | wait until T s after `rec start` (for scripted takes; logs `late by …` when behind) |
| `quit` | stop everything. Send it with `echo quit > $WORK/ctl`: it never answers `done` |

- The output is 2560×1440 at scale 2, so logical = screenshot px / 2. An image viewer that downsizes the
  screenshot changes the factor: if it shows the 2560-px image 2000 px wide, logical = displayed px × 0.64.
- Override the geometry with `MODE=2560x1440 SCALE=2 LOGICAL=1280x720` (keep `MODE = LOGICAL × SCALE`).
- Read coordinates off a fresh `shot` before every click you are unsure of. Layouts move between versions, and
  a click a few pixels off lands on nothing and reports success all the same.
- After an action that loads something (network, disk, a dialog opening), `sleep` before the `shot`. A screenshot
  taken too early shows the previous state, which is the most common false "it does not work".
- `driver.log` has every command and its `done`; `cage.log` has the app's stdout and stderr: read it when the
  window stays empty or the app exits.

## 3. Testing a change during development

1. Build the app, export `APP`, start it with `start.sh clean`.
2. Walk the flow you changed with `do.sh`, taking a `shot` at each step that should look different.
3. Look at every shot. Say what you saw, not what you expected: "the dialog opened with three rows",
   "nothing changed after the click".
4. On a bug, keep the exact command sequence that reproduces it in a file and replay it with `run.sh` after each fix.
5. `echo quit > $WORK/ctl` when done, so no headless compositor is left running.

For a moving behaviour (an animation, a progress bar, a hover state) record it instead: `rec start $WORK/rec/x.mp4`
… `rec stop`, then pull frames with `$FFMPEG -ss T -i x.mp4 -frames:v 1 frame.png` or a contact sheet
(`-vf fps=4,scale=480:-1,tile=4x4`).

## Pitfalls

- `wlrctl pointer` does not work with gpui: it creates a new virtual pointer on every call. That is why vptr exists.
- Wheel scrolling needs `axis_source(Wheel)` plus `axis_discrete`; gpui ignores a plain `axis`. vptr sends both.
- The virtual keyboard needs a full xkb keymap; tools.sh writes `vptr/keymap.xkb` with `xkbcli compile-keymap`.
  `:` and `_` are sent with Shift through the modifiers event. Other punctuation and non-Latin text are not
  mapped: add them to `code()` in `vptr/src/main.rs` if a check needs them.
- wf-recorder sometimes hangs after SIGINT though the mp4 is complete; driver.py kills it after 8 s.
- `-r 60` duplicates frames while nothing changes. That is expected, and the cursor is in the recording.
- Never `pkill -f PATTERN` where PATTERN appears in your own command line: it kills your own shell (exit 144).
  Match exactly instead: `pkill -x java`, `pgrep -f 'driver[.]py'`.
- Search fields debounce. Allow a second or more between typing and clicking a result.
- Anything the app launches (a game, a child window) runs inside the same cage session, with its Xwayland on
  `DISPLAY=:1`. Heavy OpenGL programs can crash there without a real GPU display: check them up to the launch,
  then stop the child yourself.
