# Dockerfile

FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    unzip \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Pull the model in advance (optional, improves startup time)
RUN ollama pull gemma3:1b || true

# Set working directory
WORKDIR /app

# Copy your Python app
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose Ollama's default port (11434)
# EXPOSE 11434

COPY start.sh /start.sh
RUN chmod +x /start.sh

# Start Ollama + your app (parallel)
CMD ["/start.sh"]
