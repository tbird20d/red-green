#!/bin/sh
for f in rg-user*.txt ; do
    echo "== $f =="
    cat $f
done
