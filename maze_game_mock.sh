#!/bin/sh
# Simple mock maze_game for local testing
# Usage: maze_game.sh <maze_id>

MAZE_ID="$1"
# Small fixed maze for testing (3x3 grid)
WIDTH=3
HEIGHT=3
# Start at (0,0), exit at (2,0)
X=0
Y=0
EXIT_X=2
EXIT_Y=0

# echo a startup message (optional)
# echo "maze $MAZE_ID ready"

while read -r line; do
  # expect commands like: move N
  cmd=$(echo "$line" | awk '{print $1}')
  dir=$(echo "$line" | awk '{print $2}')
  if [ "$cmd" = "move" ]; then
    nx="$X"
    ny="$Y"
    case "$dir" in
      N) ny=$((Y-1));;
      S) ny=$((Y+1));;
      E) nx=$((X+1));;
      W) nx=$((X-1));;
      *) ;;
    esac
    # Check boundaries
    if [ $nx -lt 0 ] || [ $nx -ge $WIDTH ] || [ $ny -lt 0 ] || [ $ny -ge $HEIGHT ]; then
      echo "hit wall"
      continue
    fi
    # Move
    X=$nx
    Y=$ny
    if [ "$X" -eq "$EXIT_X" ] && [ "$Y" -eq "$EXIT_Y" ]; then
      echo "reached exit"
      continue
    fi
    echo "moved"
  else
    # Unknown command: ignore
    echo "ok"
  fi
done
