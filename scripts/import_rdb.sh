#!/bin/bash

# import_rdb.sh
# Script to import an RDB file from a remote server

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
  echo "Please run as root"
  exit 1
fi

read -p "Enter Remote User (e.g. ubuntu): " REMOTE_USER
read -p "Enter Remote Host/IP: " REMOTE_HOST
read -p "Enter Remote Path to dump.rdb (default /var/lib/redis/dump.rdb): " REMOTE_PATH
REMOTE_PATH=${REMOTE_PATH:-/var/lib/redis/dump.rdb}

LOCAL_REDIS_DIR=$(redis-cli config get dir | sed -n '2p')
echo "Detected Local Redis Directory: $LOCAL_REDIS_DIR"

echo "Stopping local Redis..."
systemctl stop redis

echo "Backing up existing dump.rdb..."
if [ -f "$LOCAL_REDIS_DIR/dump.rdb" ]; then
    mv "$LOCAL_REDIS_DIR/dump.rdb" "$LOCAL_REDIS_DIR/dump.rdb.bak"
fi

echo "Downloading RDB from remote..."
scp "$REMOTE_USER@$REMOTE_HOST:$REMOTE_PATH" "$LOCAL_REDIS_DIR/dump.rdb"

if [ $? -eq 0 ]; then
    echo "Download successful."
    echo "Fixing permissions..."
    chown redis:redis "$LOCAL_REDIS_DIR/dump.rdb"
    
    echo "Starting existing Redis..."
    systemctl start redis
    echo "Done! Redis restarted with new data."
else
    echo "Download failed. Restoring backup..."
    if [ -f "$LOCAL_REDIS_DIR/dump.rdb.bak" ]; then
        mv "$LOCAL_REDIS_DIR/dump.rdb.bak" "$LOCAL_REDIS_DIR/dump.rdb"
    fi
    systemctl start redis
    exit 1
fi
