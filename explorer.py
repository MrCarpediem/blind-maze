import sys
import os
import subprocess
from typing import Dict, Tuple, List

DIRS = {
    "N": (0, -1),
    "S": (0, 1),
    "E": (1, 0),
    "W": (-1, 0),
}

OPPOSITE = {
    "N": "S",
    "S": "N",
    "E": "W",
    "W": "E",
}


class MazeExplorer:
    def __init__(self, maze_id: int):
        maze_game = "/app/maze_game.sh"

        if not os.path.exists(maze_game):
            raise RuntimeError("Run this program using `tb run` only.")

        self.proc = subprocess.Popen(
            [maze_game, str(maze_id)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            text=True,
            bufsize=1,
        )

        self.map: Dict[Tuple[int, int], str] = {}
        self.visited = set()
        self.exit_pos = None

        self.min_x = self.max_x = 0
        self.min_y = self.max_y = 0

    def _send(self, command: str) -> str:
        self.proc.stdin.write(command + "\n")
        self.proc.stdin.flush()
        return self.proc.stdout.readline().strip()

    def _update_bounds(self, x: int, y: int):
        self.min_x = min(self.min_x, x)
        self.max_x = max(self.max_x, x)
        self.min_y = min(self.min_y, y)
        self.max_y = max(self.max_y, y)

    def explore(self, x: int, y: int):
        self.visited.add((x, y))
        self.map[(x, y)] = " "
        self._update_bounds(x, y)

        for d, (dx, dy) in DIRS.items():
            nx, ny = x + dx, y + dy

            if (nx, ny) in self.visited:
                continue

            response = self._send(f"move {d}")

            if response == "hit wall":
                self.map[(nx, ny)] = "#"
                self._update_bounds(nx, ny)
                continue

            # moved OR reached exit
            self.map[(nx, ny)] = " "
            self._update_bounds(nx, ny)

            if response == "reached exit":
                self.exit_pos = (nx, ny)

            self.explore(nx, ny)

            # backtrack
            self._send(f"move {OPPOSITE[d]}")

    def _build_grid(self) -> List[List[str]]:
        width = self.max_x - self.min_x + 1
        height = self.max_y - self.min_y + 1

        grid = [["#" for _ in range(width)] for _ in range(height)]

        for (x, y), value in self.map.items():
            grid[y - self.min_y][x - self.min_x] = value

        # Start
        grid[-self.min_y][-self.min_x] = "S"

        # Exit
        if self.exit_pos:
            ex, ey = self.exit_pos
            grid[ey - self.min_y][ex - self.min_x] = "E"

        return grid

    def save_map(self, path: str):
        # add guaranteed outer walls BEFORE grid creation
        for x in range(self.min_x - 1, self.max_x + 2):
            self.map[(x, self.min_y - 1)] = "#"
            self.map[(x, self.max_y + 1)] = "#"

        for y in range(self.min_y - 1, self.max_y + 2):
            self.map[(self.min_x - 1, y)] = "#"
            self.map[(self.max_x + 1, y)] = "#"

        self.min_x -= 1
        self.max_x += 1
        self.min_y -= 1
        self.max_y += 1

        grid = self._build_grid()

        with open(path, "w") as f:
            for row in grid:
                f.write("".join(row) + "\n")


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 explorer.py <maze_id>")
        sys.exit(1)

    maze_id = int(sys.argv[1])

    explorer = MazeExplorer(maze_id)
    explorer.explore(0, 0)
    explorer.save_map(f"/app/output/{maze_id}.txt")


if __name__ == "__main__":
    main()
