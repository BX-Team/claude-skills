#!/usr/bin/env bash
# usage: do.sh 'cmd' 'cmd' ... — sends commands to driver.py and waits until each is processed
S=${WORK:?set WORK}
for c in "$@"; do
  n=$(grep -c '^done' $S/driver.log)
  echo "$c" > $S/ctl
  until [ "$(grep -c '^done' $S/driver.log)" -gt "$n" ]; do sleep 0.05; done
done
