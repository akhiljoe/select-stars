#!/bin/bash

# -----------------------------
# PostgreSQL Startup Script
# -----------------------------

DATA_DIR="/opt/homebrew/var/postgresql@18"
PG_CTL="/opt/homebrew/opt/postgresql@18/bin/pg_ctl"
PG_BIN="/opt/homebrew/opt/postgresql@18/bin/postgres"
PORT=5432

echo "-----------------------------------------"
echo "PostgreSQL Control Script"
echo "Data directory: $DATA_DIR"
echo "Port: $PORT"
echo "-----------------------------------------"

# 1️⃣ Validate installation
if [ ! -x "$PG_CTL" ]; then
    echo "Error: pg_ctl not found at $PG_CTL"
    exit 1
fi

if [ ! -d "$DATA_DIR" ]; then
    echo "Error: Data directory not found at $DATA_DIR"
    exit 1
fi

# 2️⃣ Check if server is already running (proper way)
if lsof -i :$PORT > /dev/null 2>&1; then
    echo "PostgreSQL is already running on port $PORT."
    exit 0
fi

# 3️⃣ Check for stale pid file
if [ -f "$DATA_DIR/postmaster.pid" ]; then
    echo "Warning: postmaster.pid exists but server not responding."
    echo "This may be a stale lock file."
fi

# 4️⃣ Start PostgreSQL
echo "Starting PostgreSQL..."
LC_ALL="en_US.UTF-8" $PG_CTL -D "$DATA_DIR" -l "$DATA_DIR/server.log" start

# 5️⃣ Verify startup
sleep 2

if lsof -i :$PORT > /dev/null 2>&1; then
    echo "PostgreSQL started successfully."
    echo "You can now connect using:"
    echo "  psql practice_db"
else
    echo "PostgreSQL failed to start."
    echo "Check log file:"
    echo "  $DATA_DIR/server.log"
fi

echo "-----------------------------------------"