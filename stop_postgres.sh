#!/bin/bash

# -----------------------------
# PostgreSQL Stop Script
# -----------------------------

DATA_DIR="/opt/homebrew/var/postgresql@18"
PG_CTL="/opt/homebrew/opt/postgresql@18/bin/pg_ctl"
PORT=5432

echo "-----------------------------------------"
echo "PostgreSQL Shutdown Script"
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

# 2️⃣ Check if server is actually running
if ! lsof -i :$PORT > /dev/null 2>&1; then
    echo "PostgreSQL is not running on port $PORT."
    
    # Check if stale pid file exists
    if [ -f "$DATA_DIR/postmaster.pid" ]; then
        echo "Warning: postmaster.pid exists but server not running."
        echo "This may be a stale lock file."
    fi
    
    exit 0
fi

# 3️⃣ Stop PostgreSQL (smart mode = waits for connections to close)
echo "Stopping PostgreSQL..."
$PG_CTL -D "$DATA_DIR" -m smart stop

# 4️⃣ Verify shutdown
sleep 2

if lsof -i :$PORT > /dev/null 2>&1; then
    echo "PostgreSQL did not shut down cleanly."
    echo "Trying fast shutdown..."
    $PG_CTL -D "$DATA_DIR" -m fast stop
else
    echo "PostgreSQL stopped successfully."
fi

echo "-----------------------------------------"