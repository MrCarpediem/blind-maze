#!/bin/sh
set -e

mkdir -p /app/output

for i in 1 2 3 4 5 6 7 8 9 10
do
  echo "Exploring maze $i"
  python /app/explorer.py $i
done
