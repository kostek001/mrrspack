#!/usr/bin/env bash
set -e 
set -o pipefail

dir=$(dirname "$(realpath $0)")

cd $dir/getModsHash
nix-shell --run "python main.py"

cd $dir/..
nix-shell --run "packwiz refresh"