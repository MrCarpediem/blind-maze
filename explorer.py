import sys
import os
import subprocess

DIRS = {
    "N": (0, -1),
    "S": (0, 1),
    "E": (1, 0),
    "W": (-1, 0),
}
OPP = {"N": "S", "S": "N", "E": "W", "W": "E"}

class MazeExplorer:
    def __init__(self, maze_id):
        self.proc = subprocess.Popen(
            ["./maze_game.sh", str(maze_id)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            text=True,
            bufsize=1,
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

            res = self.send(f"move {d}")
            if res == "hit wall":
                self.map[(nx, ny)] = "#"
                continue

            if res == "reached exit":
                self.exit = (nx, ny)

            self.dfs(nx, ny)
            self.send(f"move {OPP[d]}")

    def save(self, maze_id):
        xs = [x for x, _ in self.map]
        ys = [y for _, y in self.map]
        minx, maxx = min(xs)-1, max(xs)+1
        miny, maxy = min(ys)-1, max(ys)+1

        grid = []
        for y in range(miny, maxy+1):
            row = []
            for x in range(minx, maxx+1):
                row.append(self.map.get((x, y), "#"))
            grid.append(row)

        grid[-miny][-minx] = "S"
        if self.exit:
            ex, ey = self.exit
            grid[ey-miny][ex-minx] = "E"

        with open(f"output/{maze_id}.txt", "w") as f:
            for r in grid:
                f.write("".join(r) + "\n")

def main():
    maze_id = int(sys.argv[1])
    m = MazeExplorer(maze_id)
    m.dfs(0, 0)
    m.save(maze_id)

if __name__ == "__main__":
    main()
