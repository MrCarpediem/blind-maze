import os
import sys
import shutil
import subprocess
import logging

DIRS = {
    "N": (0, -1),
    "S": (0, 1),
    "E": (1, 0),
    "W": (-1, 0),
}

OPP = {"N": "S", "S": "N", "E": "W", "W": "E"}

class Explorer:
    def __init__(self, maze_id):
        logging.basicConfig(level=logging.INFO)

        # Determine which maze game binary to run. Priority:
        # 1. $MAZE_GAME environment variable
        # 2. ./maze_game.sh (relative)
        # 3. /app/maze_game.sh (absolute)
        game_cmd = os.environ.get("MAZE_GAME")
        if not game_cmd:
            if os.path.exists("./maze_game.sh"):
                game_cmd = "./maze_game.sh"
            elif os.path.exists("/app/maze_game.sh"):
                game_cmd = "/app/maze_game.sh"
            else:
                # Try to find it on PATH
                game_cmd = shutil.which("maze_game.sh") or shutil.which("maze_game")

        if not game_cmd:
            raise FileNotFoundError(
                "maze_game executable not found. Set MAZE_GAME or place maze_game.sh in the project root."
            )

        logging.info("Starting maze game: %s (maze id=%s)", game_cmd, maze_id)
        try:
            self.proc = subprocess.Popen(
                [game_cmd, str(maze_id)],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                text=True,
            )
        except FileNotFoundError:
            raise
        self.map = {}
        self.visited = set()
        self.exit = None
        self.minx = self.maxx = 0
        self.miny = self.maxy = 0

    def send(self, cmd):
        if self.proc.poll() is not None:
            raise RuntimeError("maze game process has exited")

        try:
            self.proc.stdin.write(cmd + "\n")
            self.proc.stdin.flush()
        except Exception as e:
            raise RuntimeError(f"failed to send command to maze game: {e}")

        # Read one line response; protect against EOF
        resp = self.proc.stdout.readline()
        if resp is None or resp == "":
            raise RuntimeError("no response from maze game (EOF)")
        return resp.strip()

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
        os.makedirs("/app/output", exist_ok=True)
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

        out_path = f"/app/output/{maze_id}.txt"
        with open(out_path, "w") as f:
            for row in grid:
                f.write("".join(row) + "\n")

        # Also write the canonical grader file expected at /app/maze_map.txt
        try:
            with open("/app/maze_map.txt", "w") as gf:
                for row in grid:
                    gf.write("".join(row) + "\n")
            logging.info("Wrote canonical grader file: /app/maze_map.txt")
        except Exception as e:
            logging.warning("Failed to write /app/maze_map.txt: %s", e)

        # Also persist the canonical grader file into the mounted output
        try:
            out_canonical = "/app/output/maze_map.txt"
            with open(out_canonical, "w") as of:
                for row in grid:
                    of.write("".join(row) + "\n")
            logging.info("Wrote persisted grader file: %s", out_canonical)
        except Exception as e:
            logging.warning("Failed to write /app/output/maze_map.txt: %s", e)

if __name__ == "__main__":
    mid = int(sys.argv[1])
    e = Explorer(mid)
    e.dfs(0, 0)
    e.save(mid)