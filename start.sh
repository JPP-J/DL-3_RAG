#!/bin/sh

# Start Ollama in background
ollama serve &

# Optionally wait for it to be ready (basic wait)
echo "Waiting for Ollama to be ready..."
sleep 5  # Better: ping a health endpoint

# Run the app
python app/main.py
