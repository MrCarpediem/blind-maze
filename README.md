# Blind Maze Explorer

A Depth-First Search (DFS) based solution for the TerminalBench blind maze exploration task.

## Key Features
- Fully blind exploration via CLI interaction
- DFS with explicit backtracking
- Dynamic map construction
- Deterministic output
- TerminalBench compatible

## How to run (IMPORTANT)
This project must be executed using TerminalBench:

```bash
tb run \
  --dataset terminal-bench-core==0.1.1 \
  --task-id blind-maze-explorer-algorithm \
  --agent nop \
  --model dummy
