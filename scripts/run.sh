#!/bin/sh
set -e

mkdir -p /app/output

for MAZE_ID in 1 2 3 4 5 6 7 8 9 10
do
  echo "Exploring maze $MAZE_ID"
  python explorer.py $MAZE_ID
done

echo "All mazes explored."
