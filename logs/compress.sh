#!/bin/bash
dir=$(dirname $0)
flags=""

if [ ! -d "$dir/archives" ]; then 
    mkdir "$dir/archives"
fi

if [ -f "$dir/archives/logs.zip" ]; then
    flags="-u"
fi

zip $flags "$dir/archives/logs.zip" $(find -type f -path "*.log" -not -path "*/latest.log") 