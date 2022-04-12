#!/usr/bin/env bash
set -xe


BASEDIR=/persist

export HOME=$BASEDIR/home
mkdir -p ~

export TMPDIR=$BASEDIR/tmp
mkdir -p $TMPDIR
export TMP=$TMPDIR
export TEMP=$TMPDIR
export TEMPDIR=$TMPDIR

export PYTHONUSERBASE=$BASEDIR
mkdir -p "$BASEDIR/var/log" 

export CPATH="$BASEDIR/usr/include/python3.6m/:$BASEDIR/usr/include"
export PATH="$BASEDIR/bin:/usr/bin:/bin:$PATH"

LOGFILE="session-$(date +"%Y_%m_%d_%H_%M_%S").log"

if mkdir -p /outbox 2>/dev/null; then
    LOGFILE="/outbox/$LOGFILE"
else
    LOGFILE="$BASEDIR/var/log/$LOGFILE"
fi

((

    date
    $@
    echo "EXIT CODE: $?"
    date
    tar -Jcf $LOGFILE.tar.xz /var/log/*log || true

) 2>&1 ) | tee "$LOGFILE"

exit 0
