import sys
import subprocess

DIRS = {
    "N": (0, -1),
    "S": (0, 1),
    "E": (1, 0),
    "W": (-1, 0),
}

OPP = {"N": "S", "S": "N", "E": "W", "W": "E"}

class Explorer:
    def __init__(self, maze_id):
        self.proc = subprocess.Popen(
            ["/app/maze_game.sh", str(maze_id)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            text=True,
        )
        self.map = {}
        self.visited = set()
        self.exit = None
        self.minx = self.maxx = 0
        self.miny = self.maxy = 0

    def send(self, cmd):
        self.proc.stdin.write(cmd + "\n")
        self.proc.stdin.flush()
        return self.proc.stdout.readline().strip()

    def dfs(self, x, y):
        self.visited.add((x, y))
        self.map[(x, y)] = " "
        self.minx = min(self.minx, x)
        self.maxx = max(self.maxx, x)
        self.miny = min(self.miny, y)
        self.maxy = max(self.maxy, y)

        for d, (dx, dy) in DIRS.items():
            nx, ny = x + dx, y + dy
            if (nx, ny) in self.visited:
                continue

            r = self.send(f"move {d}")
            if r == "hit wall":
                self.map[(nx, ny)] = "#"
                continue

            if r == "reached exit":
                self.exit = (nx, ny)

            self.dfs(nx, ny)
            self.send(f"move {OPP[d]}")

    def save(self, maze_id):
        for x in range(self.minx - 1, self.maxx + 2):
            self.map[(x, self.miny - 1)] = "#"
            self.map[(x, self.maxy + 1)] = "#"
        for y in range(self.miny - 1, self.maxy + 2):
            self.map[(self.minx - 1, y)] = "#"
            self.map[(self.maxx + 1, y)] = "#"

        w = self.maxx - self.minx + 3
        h = self.maxy - self.miny + 3
        grid = [["#" for _ in range(w)] for _ in range(h)]

        for (x, y), v in self.map.items():
            grid[y - self.miny + 1][x - self.minx + 1] = v

        grid[1][1] = "S"
        if self.exit:
            ex, ey = self.exit
            grid[ey - self.miny + 1][ex - self.minx + 1] = "E"

        with open(f"/app/output/{maze_id}.txt", "w") as f:
            for row in grid:
                f.write("".join(row) + "\n")

if __name__ == "__main__":
    mid = int(sys.argv[1])
    e = Explorer(mid)
    e.dfs(0, 0)
    e.save(mid)
