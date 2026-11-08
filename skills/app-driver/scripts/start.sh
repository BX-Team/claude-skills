#!/usr/bin/env bash
# usage: start.sh [clean] — (re)starts APP under headless cage with driver.py listening on $WORK/ctl.
# Needs: WORK, APP, the tool env from tools.sh; `clean` restores $WORK/home from $WORK/home.clean.
# Run from a shell that has libwayland (e.g. inside the project's `nix develop`).
set -u
S=${WORK:?set WORK}
HERE=$(cd "$(dirname "$0")" && pwd)
if pgrep -f "$HERE/driver[.]py" >/dev/null; then echo quit > $S/ctl; sleep 3; fi
if [ "${1:-}" = clean ]; then rm -rf $S/home && cp -a $S/home.clean $S/home; fi
mkdir -p $S/rec $S/shots
: > $S/driver.log
nohup ${PYTHON:-python3} $HERE/driver.py >/dev/null 2>&1 &
until grep -q ready $S/driver.log; do sleep 0.3; done
sleep 4
