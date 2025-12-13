FROM python:3.11-slim

WORKDIR /app

# Copy the explorer script
COPY explorer.py .
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

# Install TerminalBench for running the project
RUN pip install --no-cache-dir terminal-bench-core==0.1.1

# Default command - show usage
CMD ["echo", "This is a TerminalBench project. Use: tb run --dataset terminal-bench-core==0.1.1 --task-id blind-maze-explorer-algorithm --agent nop --model dummy"]
