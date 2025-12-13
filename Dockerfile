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

# Default command - display usage info
CMD ["echo", "Blind Maze Explorer - Ready to run with TerminalBench or standalone"]
