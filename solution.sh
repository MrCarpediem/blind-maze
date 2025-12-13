#!/bin/sh
set -e

echo "=== SOLUTION STARTED ==="

mkdir -p /app/output

for i in 1 2 3 4 5 6 7 8 9 10
do
  echo "Solving maze $i"
  python /app/explorer.py $i
done

echo "=== OUTPUT FILES ==="
ls -l /app/output
