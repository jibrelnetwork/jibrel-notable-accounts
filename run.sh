#!/bin/sh -e

echo "Starting Jibrel Notable Accounts service, mode '$1' version: $(cat /app/version.txt) on node $(hostname)"

exec "$@"
