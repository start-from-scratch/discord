#!/bin/bash
ROOT=$(dirname $0)
TMPDIR=$(mktemp -d)

for FILE in $(find $ROOT -type f -path "*.log"); do
    TIMESTAMP=$(stat -c "%W" "$ROOT/latest.log")
    mv "$FILE" "$TMPDIR/$TIMESTAMP.log"
done

printf "" > "$ROOT/latest.log"
$ROOT/compress.sh $TMPDIR