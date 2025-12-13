FROM python:3.11-slim

# Runtime image for the Blind Maze Explorer agent.
# This image is intended for running the explorer in a grader or
# local development environment. It does not include task test harnesses.

WORKDIR /app

# Copy the runtime artifacts (explorer and a developer runner)
COPY explorer.py .
COPY dev-solution.sh .
COPY README.md .

# Create output directory (mounted by the host during runs)
RUN mkdir -p /app/output

# Install any minimal runtime dependencies (kept small for grader images)
RUN apt-get update && apt-get install -y --no-install-recommends \
    bash \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Make the dev runner executable
RUN chmod +x dev-solution.sh

# The image does NOT include the local development mock `maze_game_mock.sh`.
# In the grader environment the real `maze_game.sh` will be provided.

# Default command: print brief usage. Use `docker run ... /app/dev-solution.sh` to run.
CMD ["echo", "Blind Maze Explorer - Ready to run with TerminalBench or standalone"]
