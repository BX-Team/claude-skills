---
name: app-promo-video
description: Make a promo, teaser or showcase video of a desktop GUI app (gpui or any Wayland app) from a real recording of the app being used (clicks, typing, tab switches), with a smooth camera, captions, a logo intro and outro, and generated royalty-free music. Use when asked for a promo video, teaser, trailer, showcase or demo video of an app. Records through the app-driver skill. Linux with Nix.
---

# App promo video from a real recording

The reference result is the Riven Launcher teaser: 45 s, 1920×1080 at 60 fps, calm half-time music, the app
working for real on a dark animated backdrop. It is **one continuous take recorded in real time on the video's
own timeline** (no speed-ups, no cuts), with a camera that glides in on the action, one caption per scene, a logo
intro, and a logo + link outro.

Pipeline: **sandboxed data → warm caches → beat schedule → real-time take → music → render** (camera and captions
over the take, 1:1). Everything runs off-screen.

Why one real-time take: recording loosely and then time-warping clicks onto beats, hiding the waits with soft
cuts, was tried first and rejected: the speed changes and dissolves were visible. It survives only as a fallback
(§5b).

```
scripts/
  schedule.py  beat-timed schedule → driver take whose every click lands on its beat (`at T` commands)
  music.py     calm track generator (BARS × 1.875 s; 24 bars = 45 s)
  render.py    the edit: intro, scenes, camera, captions, click rings, outro → mp4 with the music
  camcheck.py  checks the camera for jumps and prints each scene's playback speed
reference/
  riven-schedule.txt           the 45 s take
  riven-schedule-long-a/-b.txt a 62 s cut in two takes (a cold install happens between them, off-camera)
  riven-plan.py                the edit plan render.py reads: title, tagline, link, scenes and camera keys
  riven-take.events.jsonl      the event log of the 45 s take, for REF_EVENTS
```

The Riven UI was in Russian when those takes were shot; the button names in the schedule comments and the
captions in the plan are translated.

## 1. Setup

Recording is done by the **app-driver** skill, the sibling directory of this one. Read its SKILL.md first: the
sandboxing rules, the command table and its pitfalls all apply here.

```bash
export DRIVER=<app-driver skill dir>/scripts PROMO=<this skill dir>/scripts
export WORK=<a scratch dir> APP=/path/to/release/binary
eval "$($DRIVER/tools.sh)"            # also provides FFMPEG and a PYTHON with numpy/pillow/scipy
```

- Use a release build: a debug gpui build is too slow to look smooth.
- Get the state right first (the items to feature, theme, selection, onboarding finished, nothing that shows a
  warning), then freeze it: `cp -a $WORK/home $WORK/home.clean`. Every take starts with `start.sh clean`.
- Ask the user which content to feature. Whatever gets installed or created during the take must NOT already
  exist in `home.clean`.
- To show the user's own account, copy only its public entry (id, name, avatar), never tokens. Without tokens,
  an action that needs sign-in shows an error just after the click, so end that scene frozen on the pressed
  button: `take_seg(…, hold=T)` with T the event time of the last frame before the message (find it frame by
  frame after the click).

## 2. Explore

`start.sh clean`, then `do.sh` and `shot` (see app-driver) until you know every coordinate of the flow. Write the
coordinates down as you go: the schedule is made of them.

## 3. Record the take: one real-time take on the timeline

1. **Write the schedule in beats** (see `reference/riven-schedule.txt`): `BEAT ACTION ARGS`, where the beat is the
   VIDEO beat the click or key press lands on (B(n) = n × 60/128 s; the app part runs from beat 8 to the outro at
   beat 88 for 45 s). Give each action at least 1.5–2 beats; moves arrive on their beat; `down`/`up` make drags.
   `$PYTHON $PROMO/schedule.py schedule.txt > take.run` (env `TAKE`, `WORK`; `E0` = pre-roll, default 4 s) turns
   it into `at`-timed driver commands, so the event clock maps to video time 1:1:
   `event = E0 + (beat − 8) × BEAT`.
2. **Warm every cache first.** Network-bound steps (search, details, installs) vary from 0.6 s to 5 s cold, and a
   click then lands on a stale list or a still-disabled button. Do one full run of the network steps off-camera,
   then copy the app's caches from `$WORK/home` into `$WORK/home.clean` (but NOT what was installed). Caches
   expire (Riven's API cache lives an hour): record right after warming.
3. **Rehearse, then record**: `start.sh clean; run.sh take.run; echo quit > $WORK/ctl`. Check `driver.log` for
   `late by` (a few 0.03–0.05 s are fine), then make a contact sheet of the take at every scheduled click. If
   anything landed wrong (a dialog still open, a list not loaded), move that beat later and record again. Never
   patch it in the edit.

Contact sheets: `$FFMPEG -ss T -i take.mp4 -frames:v 1 -vf scale=480:270,drawtext=…` per time, then `tile=4x4`.
Video time T in the raw take ≈ event time (render.py measures the exact offset, see Pitfalls).

## 4. Music

`$PYTHON $PROMO/music.py $WORK/music.wav` makes a calm D-major track (Dmaj9–Bm9–Gmaj9–A6/9): pad, electric
piano, legato sine bass, half-time soft kick + rim + shaker, a bell melody from bar 6, fuller from bar 14, a final
chord at bar BARS−2 under the outro. Grid 128 BPM (feels like 64). Length = `BARS` × 1.875 s. A longer cut:
`BARS=36 FULL=17` (FULL = the bar where the second bell voice joins; `BARS=24 FULL=14` is the 45 s track).
**Regenerate, never time-stretch.** Check it with `$FFMPEG -i music.wav -af ebur128` (≈ −11…−12 LUFS) and
`showwavespic` (no dips at bar ends). You cannot listen to it: say so, the user judges the music.

## 5. Edit plan

The plan is a Python file render.py reads from `PLAN` (default `reference/riven-plan.py`). Copy the reference
into `$WORK` and rewrite it. It sets `TITLE`, `TAGLINE` and `LINK` for the intro and the outro, and `SEGMENTS`.
Times are in beats, `B(n) = n × 60/128`. The intro is bars 0–1 (B(0)–B(8)); the outro starts at bar BARS−2.
With a scheduled take each scene is just

```python
take_seg(b0, b1, cam=[(B(beat), cx, cy, zoom), …], caption=("Title", "subtitle"))
```

which plays the take 1:1 (anchor `E0 + (b0 − 8) × BEAT` → `B(b0)`). Every join between scenes is continuous, so
the whole app part is one take with one camera path, and the captions simply change at scene borders. Start a
scene's caption on, or just before, its first click.

- **Camera keys** are targets (logical cx, cy; zoom 1.0 = the whole window at 1500 px wide). They are joined
  linearly and then Gaussian-smoothed (σ 0.45 s, zoom in log space), so the camera never stops on a key. Keep
  zoom ≤ 1.75, hold the first key about a beat after the intro, leave ≥ 1.5 beats between big moves, and frame
  where the cursor is going one beat before the click.
- Run `$PYTHON $PROMO/camcheck.py`: every speed must read 1.00×; window changes peak at ≈ 20–30 px/frame; a lone
  spike is a jump.
- Captions sit bottom-left with an accent bar and reveal word by word.

### 5b. Fallback: a time-warped loose take

`seg(v0, v1, anchors=[(raw_event_time, B(beat)), …], s0, s1, cam, caption)` warps a loosely recorded take so its
clicks land on beats. Joins that are not continuous become one-window dissolves (`XFADE` 0.8 s). `REF_EVENTS`
remaps a plan's anchors onto a re-recorded take by matching events. Use it only when a real-time take is
impossible, and keep it ≤ 1.7×.

### Waits that are too long to show

A long wait (a first install of a big pack) is never recorded and never sped up. Take A ends while the progress
runs, the work finishes off-camera, take B starts from the finished state: `TAKE=a,b`, take B's schedule uses
`FIRST_BEAT=` its first beat, its scenes pass `take=1, first=…`, and the first of them sets
`skip_label="≈ 1.5 minutes later"`, which renders a dimmed dissolve under a pill. Do not record through the wait
either: wf-recorder dropped seconds of frames under that load.

## 6. Render

```bash
export TAKE=take PLAN=$WORK/plan.py MUSIC=$WORK/music.wav LOGO=<square RGBA png> \
  FONT=<InterVariable.ttf> NERD_FONT=<any Nerd Font .ttf>   # the GitHub glyph U+F09B
PREVIEW=3.0,10.5,27.3 $PYTHON $PROMO/render.py         # stills → $WORK/preview/
$PYTHON $PROMO/render.py $WORK/teaser.mp4              # the full video: ~2 min for 45 s on 12 cores
```

The first run extracts the frames it needs to `$WORK/cache/$TAKE` (JPEG q95). Then make a contact sheet of the
result around every cut and every beat-locked click (the UI change should land within a frame or two of the
beat), and copy the final file where the user wants it (`~/Videos/` unless told otherwise). `$WORK` usually lives
in a session scratch directory: keep the schedule and the plan somewhere lasting if a re-shoot is likely.

## House style (keep it unless the user asks otherwise)

- A dark navy backdrop with three slow blurred blobs and faint tide lines; the window with rounded corners, a
  soft shadow, a faint blue glow and a border. The accent colour is `ACCENT` in render.py.
- Intro: the logo scales in, the title appears letter by letter, the tagline on bar 1; a blurred copy of the app
  behind sharpens and grows into the first scene's exact framing, with no cut.
- Click feedback: an expanding accent ring and a small white dot. The real cursor, with its hover shapes, is in
  the recording.
- Outro: the window shrinks away, then the logo and the name, then the GitHub glyph and `LINK`.
- **Rejected, do not bring back**: energetic or EDM music, white flashes, zoom pulsing on the beat, flash-cut
  montages, grey feature chips in the outro, 30 s versions where things run 3–5× fast, anything sped up to look
  instant (an install that "finished in seconds" only because the store was warm was rejected).
- Captions name what the viewer sees and what it gives them ("Everything downloads itself"), not what the app
  does not do. Riven's are in `reference/riven-plan.py`.

## Pitfalls

- **Sync** between the event clock and the recording: render.py finds `REC_LAG` by matching frames that change
  against logged cursor moves (cached in `take.mp4.lag`); it is ≈ 0. Do NOT derive it from
  `last event − video duration`: when wf-recorder hangs on exit the file loses its tail (2.3 s once), and the
  click rings then appear seconds before the cursor gets there.
- Window placement must be continuous: an `if window wider than frame` branch made the image jump when the zoom
  crossed the threshold. Separately smoothed tracks for one continuous take also jump at the join.
- A plain cross-dissolve of two differently zoomed windows looks dirty: dissolve the content inside one window.
- Typing runs ~0.135 s per character (not schedule.py's 0.11): a 35-character URL takes ~10 beats. Schedule the
  next click after that, or every later click shifts (`late by` 0.8 s and more).
- Search fields debounce: even with a warm cache allow ≥ 3 beats (1.4 s) between typing and clicking a result.
- Links typed on camera must look real. Do an import from a localhost URL off-camera; on screen it looks bad.
- Re-shooting for a new version: the old `$WORK` is usually gone. Rebuild `home.clean` from the user's real data
  (caches and stores, plus only the featured items, never tokens), build the release binary AT THE RELEASE TAG
  (the version shows in the app), and re-check every coordinate with shots: rows move between versions.

### Riven Launcher specifics

The reference takes hit these; they are typical of any launcher or package-manager UI.

- Pack links must be http(s). Serve a local `dist/` with `python3 -m http.server 8765 --bind 127.0.0.1`.
- Clicking Play really launches the game inside cage; heavy modpacks crash there without a real display, so end
  on the launch progress and `pkill -x java` afterwards.
- An install took 3.8–5 s even warm: schedule the next click ≥ 6 s after Install. Pressing Done in "Add mods"
  while it installs CANCELS the install: wait ~3 s (warm) before it.
- A Riven channel link checks in ~1.5–3 s and shows the optional groups; a GitHub repository link downloads the
  150 MB release first (~20 s). Click optional-group toggles ≥ 2 beats after the preview appears.
- The memory slider is at the bottom of the Java page: scroll the page first, over an empty area, not the Java list.
