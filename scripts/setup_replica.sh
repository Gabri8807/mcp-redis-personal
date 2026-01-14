#!/bin/bash

# setup_replica.sh
# Script to configure this server as a Replica of another Redis instance

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
  echo "Please run as root"
  exit 1
fi

read -p "Enter Master Redis IP: " MASTER_IP
read -p "Enter Master Redis Port (default 6379): " MASTER_PORT
MASTER_PORT=${MASTER_PORT:-6379}
read -p "Enter Master Redis Password (leave empty if none): " MASTER_PASS

echo "Configuring this server to replicate $MASTER_IP:$MASTER_PORT..."

# Configure Replica
if [ -z "$MASTER_PASS" ]; then
    redis-cli replicaof "$MASTER_IP" "$MASTER_PORT"
else
    redis-cli config set masterauth "$MASTER_PASS"
    redis-cli replicaof "$MASTER_IP" "$MASTER_PORT"
fi

echo "Replica configuration sent."
echo "Checking status..."
sleep 2
redis-cli info replication

echo ""
echo "To stop replication and make this server independent, run: redis-cli replicaof no one"
