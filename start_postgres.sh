#!/bin/bash

DATA_DIR="/opt/homebrew/var/postgresql@18"
PG_CTL="/opt/homebrew/opt/postgresql@18/bin/pg_ctl"

if [ -f "$DATA_DIR/postmaster.pid" ]; then
    echo "PostgreSQL is already running."
else
    echo "Starting PostgreSQL..."
    LC_ALL="en_US.UTF-8" $PG_CTL -D $DATA_DIR start
fi
