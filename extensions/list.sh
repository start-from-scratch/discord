#!/bin/bash
ROOT=$(dirname $0)

printf "" > "$ROOT/scripts/list.txt"

for FILE in $(find "$ROOT/scripts" -type f -path "*.py" -not -path "*/.*"); do
    PATH=$(realpath -m --relative-to=$1 $FILE)
    PATH=${PATH%.*}
    PATH=${PATH////.}
    echo $PATH >> "$ROOT/scripts/list.txt"
done