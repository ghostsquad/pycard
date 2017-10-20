#!/usr/bin/env bash

set -e

if [ "$1" == "pycard" ]; then
    shift;
    exec python pycard.py --port 80 $@
else
    exec $@
fi
