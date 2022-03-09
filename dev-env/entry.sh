#!/usr/bin/env bash
set -xe

BASEDIR=/persist

export PYTHONUSERBASE=$BASEDIR
mkdir -p "$BASEDIR/var/log" 

export CPATH="$BASEDIR/usr/include/python3.6m/:$BASEDIR/usr/include"
export PATH="$BASEDIR/bin:$PATH"

LOGFILE="session-$(date +"%Y_%m_%d_%H_%M_%S").log"

if mkdir -p /outbox 2>/dev/null; then
    LOGFILE="/outbox/$LOGFILE"
else
    LOGFILE="$BASEDIR/var/log/$LOGFILE"
fi

((

    date
    $@
    date

) 2>&1 ) | tee "$LOGFILE"

exit 0
