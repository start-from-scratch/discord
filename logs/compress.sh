#!/bin/bash
ROOT=$(dirname $0)
FLAGS="-j"

if [ -f "$ROOT/logs.zip" ]; then
    FLAGS+=" -u"
fi

zip $FLAGS "$ROOT/logs.zip" $1/*