import subprocess
from typing import Dict, Tuple, Set, List


class MazeExplorer:
    """Blind maze exploration using DFS with backtracking."""

    DIRECTIONS = {
        "N": (0, -1),
        "E": (1, 0),
        "S": (0, 1),
        "W": (-1, 0),
    }

    OPPOSITE = {
        "N": "S",
        "S": "N",
        "E": "W",
        "W": "E",
    }

    def __init__(self):
        self.map: Dict[Tuple[int, int], str] = {(0, 0): "S"}
        self.visited: Set[Tuple[int, int]] = set()

        self.x = 0
        self.y = 0

        self.min_x = self.max_x = 0
        self.min_y = self.max_y = 0

        self.process = subprocess.Popen(
            ["maze_game.sh"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            text=True,
        )

    def _send(self, command: str) -> str:
        self.process.stdin.write(command + "\n")
        self.process.stdin.flush()
        return self.process.stdout.readline().strip()

    def _update_bounds(self, x: int, y: int) -> None:
        self.min_x = min(self.min_x, x)
        self.max_x = max(self.max_x, x)
        self.min_y = min(self.min_y, y)
        self.max_y = max(self.max_y, y)

    def explore(self, x: int, y: int) -> None:
        self.visited.add((x, y))

        for direction, (dx, dy) in self.DIRECTIONS.items():
            nx, ny = x + dx, y + dy

            if (nx, ny) in self.visited:
                continue

            response = self._send(f"move {direction}")

            if "hit wall" in response:
                self.map[(nx, ny)] = "#"
                continue

            self.x, self.y = nx, ny
            self.map[(nx, ny)] = "E" if "reached exit" in response else " "
            self._update_bounds(nx, ny)

            self.explore(nx, ny)

            self._send(f"move {self.OPPOSITE[direction]}")
            self.x, self.y = x, y

    def _build_grid(self) -> List[List[str]]:
        width = self.max_x - self.min_x + 1
        height = self.max_y - self.min_y + 1

        grid = [["#"] * width for _ in range(height)]
        for (x, y), value in self.map.items():
            grid[y - self.min_y][x - self.min_x] = value

        return grid

    def save_map(self, path: str) -> None:
        # Add guaranteed outer walls
        for x in range(self.min_x - 1, self.max_x + 2):
            self.map.setdefault((x, self.min_y - 1), "#")
            self.map.setdefault((x, self.max_y + 1), "#")

        for y in range(self.min_y - 1, self.max_y + 2):
            self.map.setdefault((self.min_x - 1, y), "#")
            self.map.setdefault((self.max_x + 1, y), "#")

        grid = self._build_grid()

        with open(path, "w") as f:
            for row in grid:
                f.write("".join(row) + "\n")

        self._send("exit")
