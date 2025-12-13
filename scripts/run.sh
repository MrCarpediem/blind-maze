#!/bin/sh
set -e

mkdir -p output

for i in 1 2 3 4 5 6 7 8 9 10
do
  echo "Exploring maze $i"
  python3 explorer.py $i
done

echo "All mazes explored successfully."
