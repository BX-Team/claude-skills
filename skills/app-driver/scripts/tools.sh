#!/usr/bin/env bash
# usage: eval "$(tools.sh)" — builds the tools through nix (cached after the first run) and the vptr
# input driver, then prints the exports the other scripts read.
set -euo pipefail
HERE=$(cd "$(dirname "$0")" && pwd)
p() { nix build --no-link --print-out-paths "nixpkgs#$1" 2>/dev/null | grep -v -- '-man$' | head -n 1; }
CAGE=$(p cage)/bin/cage
GRIM=$(p grim)/bin/grim
RANDR=$(p wlr-randr)/bin/wlr-randr
WFREC=$(p wf-recorder)/bin/wf-recorder
FF=$(nix build --no-link --print-out-paths nixpkgs#ffmpeg-full.bin 2>/dev/null | head -n 1)/bin
PY=$(nix build --no-link --print-out-paths --impure --expr 'with import <nixpkgs> {}; python3.withPackages (p: [p.numpy p.pillow p.scipy])' 2>/dev/null)/bin/python3
if [ ! -x "$HERE/vptr/target/release/vptr" ]; then
  nix shell nixpkgs#libxkbcommon -c xkbcli compile-keymap --layout us > "$HERE/vptr/keymap.xkb"
  (cd "$HERE/vptr" && nix shell nixpkgs#cargo nixpkgs#rustc nixpkgs#pkg-config nixpkgs#wayland -c cargo build --release -q) >&2
fi
cat <<EOF
export CAGE=$CAGE GRIM=$GRIM WLR_RANDR=$RANDR WF_RECORDER=$WFREC
export FFMPEG=$FF/ffmpeg FFPROBE=$FF/ffprobe PYTHON=$PY
EOF
