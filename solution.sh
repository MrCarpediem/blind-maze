#!/bin/sh
set -e

echo "=== SOLUTION.SH STARTED ==="
pwd
ls -la

mkdir -p output
echo "Created output directory"

for MAZE_ID in 1 2 3 4 5 6 7 8 9 10
do
  echo "Running maze $MAZE_ID"
  python explorer.py $MAZE_ID
done

echo "=== SOLUTION.SH FINISHED ==="
ls -la output
