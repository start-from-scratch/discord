#!/bin/bash
dir=$(dirname $0)

if [ -f "$dir/latest.log" ]; then
    file="$dir/$(cat "$dir/latest.log" | head -n 1 | sed 's/\r$//').log"
    cp "$dir/latest.log" $file
    $dir/compress.sh
    rm $file
fi

echo $(date +%s) > "$dir/latest.log"