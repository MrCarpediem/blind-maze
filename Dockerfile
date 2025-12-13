FROM python:3.11-slim

WORKDIR /app

# Copy the explorer script
COPY explorer.py .
COPY solution.sh .

# Create output directory
RUN mkdir -p /app/output

# Install any dependencies (if needed)
RUN apt-get update && apt-get install -y --no-install-recommends \
    bash \
    && rm -rf /var/lib/apt/lists/*

# Make solution script executable
RUN chmod +x solution.sh

# Set the default command
CMD ["python", "explorer.py"]
