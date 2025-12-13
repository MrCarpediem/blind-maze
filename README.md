# Blind Maze Explorer

A Depth-First Search (DFS) based solution for the TerminalBench blind maze exploration task.

## Key Features
- Fully blind exploration via CLI interaction
- DFS with explicit backtracking
- Dynamic map construction
- Deterministic output
- TerminalBench compatible
- Docker-ready

## How to run with TerminalBench (Recommended)

Install TerminalBench first:
```bash
pip install terminal-bench
```

Then run:
```bash
tb run \
  --dataset terminal-bench-core==0.1.1 \
  --task-id blind-maze-explorer-algorithm \
  --agent nop \
  --model dummy
```

## How to run with Docker

Start an interactive Docker shell:
```bash
docker compose up
```

Inside the container, you can:
- Run TerminalBench: `tb run --dataset terminal-bench-core==0.1.1 --task-id blind-maze-explorer-algorithm --agent nop --model dummy`
- Or run directly: `python explorer.py <maze_id>`

To exit: `exit`

Or run a one-shot command:
```bash
docker run -v $(pwd)/runs:/app/runs -v $(pwd)/output:/app/output blind-maze-explorer python explorer.py 1
```

## Project Structure

- `explorer.py` - Main DFS-based maze explorer
- `solution.sh` - Shell script for running multiple maze instances
- `Dockerfile` - Docker configuration
- `docker-compose.yml` - Docker Compose orchestration

