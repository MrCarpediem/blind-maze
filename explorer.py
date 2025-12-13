import sys
import os
import subprocess
from typing import Dict, Tuple

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
            raise RuntimeError("Run using TerminalBench only")

        self.proc = subprocess.Popen(
            [maze_game, str(maze_id)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            text=True,
            bufsize=1,
        )

        # (x,y) -> {dir: "#"/" "}
        self.cells: Dict[Tuple[int, int], Dict[str, str]] = {}
        self.fully_explored = set()
        self.exit_pos = None

        self.min_x = self.max_x = 0
        self.min_y = self.max_y = 0

    def _send(self, cmd: str) -> str:
        self.proc.stdin.write(cmd + "\n")
        self.proc.stdin.flush()
        return self.proc.stdout.readline().strip()

    def _update_bounds(self, x: int, y: int):
        self.min_x = min(self.min_x, x)
        self.max_x = max(self.max_x, x)
        self.min_y = min(self.min_y, y)
        self.max_y = max(self.max_y, y)

    def explore(self, x: int, y: int):
        if (x, y) not in self.cells:
            self.cells[(x, y)] = {}

        self._update_bounds(x, y)

        for d, (dx, dy) in DIRS.items():
            if d in self.cells[(x, y)]:
                continue  # already probed

            nx, ny = x + dx, y + dy
            response = self._send(f"move {d}")

            if response == "hit wall":
                self.cells[(x, y)][d] = "#"
                continue

            # moved or reached exit
            self.cells[(x, y)][d] = " "
            if (nx, ny) not in self.cells:
                self.cells[(nx, ny)] = {}

            self.cells[(nx, ny)][OPPOSITE[d]] = " "

            if response == "reached exit":
                self.exit_pos = (nx, ny)

            self.explore(nx, ny)
            self._send(f"move {OPPOSITE[d]}")

        self.fully_explored.add((x, y))

    def build_grid(self):
        width = (self.max_x - self.min_x + 1) * 2 + 1
        height = (self.max_y - self.min_y + 1) * 2 + 1

        grid = [["#" for _ in range(width)] for _ in range(height)]

        def gx(x): return (x - self.min_x) * 2 + 1
        def gy(y): return (y - self.min_y) * 2 + 1

        for (x, y), walls in self.cells.items():
            cx, cy = gx(x), gy(y)
            grid[cy][cx] = " "

            for d, v in walls.items():
                dx, dy = DIRS[d]
                grid[cy + dy][cx + dx] = v

        sx, sy = gx(0), gy(0)
        grid[sy][sx] = "S"

        if self.exit_pos:
            ex, ey = self.exit_pos
            grid[gy(ey)][gx(ex)] = "E"

        return grid

    def save(self, maze_id: int):
        grid = self.build_grid()
        with open(f"/app/output/{maze_id}.txt", "w") as f:
            for row in grid:
                f.write("".join(row) + "\n")


def main():
    maze_id = int(sys.argv[1])
    explorer = MazeExplorer(maze_id)
    explorer.explore(0, 0)
    explorer.save(maze_id)


if __name__ == "__main__":
    main()
