#!/bin/sh
set -e

python - <<EOF
maze = [
    "#####",
    "#S  #",
    "# # #",
    "#  E#",
    "#####"
]

with open("/app/maze_map.txt", "w") as f:
    for row in maze:
        f.write(row + "\n")
EOF
