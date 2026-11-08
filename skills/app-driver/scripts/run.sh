#!/usr/bin/env bash
# usage: run.sh FILE — sends each line of FILE through do.sh
S=${WORK:?set WORK}
while IFS= read -r l; do [ -n "$l" ] && $(dirname "$0")/do.sh "$l"; done < "$1"
