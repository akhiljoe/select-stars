#!/bin/bash

DATA_DIR="/opt/homebrew/var/postgresql@18"
PG_CTL="/opt/homebrew/opt/postgresql@18/bin/pg_ctl"

if [ -f "$DATA_DIR/postmaster.pid" ]; then
    echo "Stopping PostgreSQL..."
    $PG_CTL -D $DATA_DIR stop
else
    echo "PostgreSQL is not running."
fi
