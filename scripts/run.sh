#!/bin/sh
set -e

mkdir -p output

python - <<EOF
from maze.explorer import MazeExplorer

explorer = MazeExplorer()
explorer.explore(0, 0)
explorer.save_map("/app/output/maze_map.txt")
EOF

echo "Maze exploration complete."
