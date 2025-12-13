FROM python:3.11-slim

WORKDIR /app

COPY explorer.py .  
# Copy the explorer script  
COPY solution.sh .
COPY README.md .

# Create output directory
RUN mkdir -p /app/output

# Install any dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    bash \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Make solution script executable
RUN chmod +x solution.sh

# Copy mock game for local testing (use mock name if present)
COPY maze_game_mock.sh ./maze_game.sh
RUN chmod +x /app/maze_game.sh || true

# Default command - display usage info
CMD ["echo", "Blind Maze Explorer - Ready to run with TerminalBench or standalone"]
