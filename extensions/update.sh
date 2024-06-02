#!/bin/bash
ROOT=$(dirname $0)

# $1 = config file path
jq -r -s ".[0] | .extensions[]|[.name, .repository, .scripts] | @tsv" $1 | 
while IFS=$'\t' read -r name repository scripts; do
    DIR=$(mktemp -d)

    git clone "$repository" "$DIR"

    if [ ! -d "$ROOT/scripts/$name" ]; then
        mkdir "$ROOT/scripts/$name"
    fi
    
    mv $DIR$scripts/* "$ROOT/scripts/$name/"
done

$ROOT/list.sh $(dirname $1)