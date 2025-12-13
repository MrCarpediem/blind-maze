#!/bin/sh
set -e

mkdir -p /app/output

for MAZE_ID in 1 2 3 4 5 6 7 8 9 10
do
  python3 /app/explorer.py $MAZE_ID
done
