# Blind Maze Explorer

Lightweight DFS-based maze exploration agent designed for the TerminalBench "blind maze" task. The project contains a local mock for development and also supports running inside Docker.

Goal: fully explore an unknown maze using only CLI move commands and produce a final map file at `/app/maze_map.txt` (also persisted to `./output/maze_map.txt`).

Quick overview
- **Language:** Python 3.11
- **Primary scripts:** `explorer.py` (agent), `solution.sh` (runner)
- **Local testing:** `maze_game.sh` (mock game included for dev)
- **Containerized:** `Dockerfile` + `docker-compose.yml`

Requirements
- Docker (for the containerized workflow) or Python 3.11+ for local runs.

Quick start — Docker (recommended)

1. Build the image (from project root):
```bash
docker compose build
```

2. Run the one-shot runner (runs mazes 1..10 and writes outputs):
```bash
docker compose run --rm maze-explorer /app/solution.sh
```

3. Inspect results on the host:
```bash
ls -l output
cat output/maze_map.txt    # canonical grader file
cat output/1.txt           # per-maze output
```

Quick start — Local (no Docker)

1. Ensure Python 3.11+ is installed.
2. Make the mock executable and run a single maze:
```bash
chmod +x maze_game.sh
python explorer.py 1
```
This writes `/app/output/1.txt` (create `/app/output` first if necessary) and `/app/maze_map.txt`.

Running with TerminalBench (if you have it)

If you have TerminalBench available and want to run the official harness instead of the mock:
```bash
pip install terminal-bench
tb run \
  --dataset terminal-bench-core==0.1.1 \
  --task-id blind-maze-explorer-algorithm \
  --agent nop \
  --model dummy
```

Files and responsibilities
- `explorer.py`: agent implementation. Finds `maze_game.sh` (via `MAZE_GAME`, `./maze_game.sh`, `/app/maze_game.sh`, or PATH), runs DFS, writes `/app/output/<id>.txt` and canonical `/app/maze_map.txt` (and a persisted copy `/app/output/maze_map.txt`).
- `solution.sh`: convenience runner that executes the explorer across multiple maze ids and ensures the canonical map is persisted.
- `maze_game.sh`: local mock (development only). The grader provides its own game during evaluation.
- `Dockerfile`, `docker-compose.yml`: container configuration. `docker compose run` uses `maze-explorer` service which mounts `./output` so results are visible on the host.

Troubleshooting
- If `docker compose` is not found, install Docker Desktop or Docker Engine with Compose v2.
- If the grader reports `maze_map.txt` missing:
  - Confirm `output/maze_map.txt` exists locally after a run.
  - Ensure your agent writes `/app/maze_map.txt` (explorer does this by default).
- If explorer fails to start complaining `maze_game.sh` not found, set `MAZE_GAME` to the correct path or place `maze_game.sh` in the project root:
  ```bash
  export MAZE_GAME=/full/path/to/maze_game.sh
  ```

What to submit
- The repo root (all source files) or the Docker image. For grader/CI, the key artifact is that `/app/maze_map.txt` is present and correct after your agent runs.

Contact / next steps
- If you want, I can add a GitHub Actions CI workflow that builds the Docker image and runs a smoke test automatically on push.

---
Small note: remove the local `maze_game.sh` mock before final submission if the grader provides its own game to avoid confusion.

