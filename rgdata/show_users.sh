#!/bin/sh
for f in users/* ; do
    echo "== $f =="
    cat $f
done
