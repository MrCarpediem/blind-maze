# Blind Maze Explorer

An industry-style implementation of a blind maze exploration agent.

The agent has **no prior knowledge** of the maze layout, size, or exit
location. It interacts only through movement commands and textual
feedback, simulating a real-world black-box environment.

---

## Key Features

- Depth-First Search (DFS) with safe backtracking
- Relative coordinate system (origin-agnostic)
- Deterministic full-map reconstruction
- Clear separation of logic and execution
- Fully Dockerized for reproducibility

---

## How It Works

1. Start from an unknown position (`S`)
2. Explore all reachable paths using DFS
3. Detect walls and open paths from command feedback
4. Track coordinates relative to the start position
5. Normalize coordinates to reconstruct the full maze
6. Save the final map to a file

The exploration **does not stop at the exit** (`E`); the entire maze
is explored before generating the final map.

---

## Project Structure

