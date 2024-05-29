#!/bin/bash
ROOT=$(dirname $0)

if [ -f "$ROOT/latest.log" ]; then
    TIMESTAMP=$(stat -c "%W" "$ROOT/latest.log")
    TMPFILE=$(mktemp "/tmp/$TIMESTAMP.XXXXXX")
    
    echo $(cat "$ROOT/latest.log") > "$TMPFILE"
    rm "$ROOT/latest.log"

    $ROOT/compress.sh $TMPFILE
fi