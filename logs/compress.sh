#!/bin/bash
ROOT=$(dirname $0)
FLAGS="-j"

FILE=$(basename $1)
FILE="$ROOT/${FILE%.*}.log"
ln -s "$1" "$FILE"

if [ ! -d "$ROOT/archives" ]; then 
    mkdir "$ROOT/archives"
fi

if [ -f "$ROOT/archives/logs.zip" ]; then
    FLAGS+=" -u"
fi

zip $FLAGS "$ROOT/archives/logs.zip" "$FILE"
rm $FILE