#!/bin/bash

# Run any setup for system
echo "Starting system..."

uvicorn app:app --host 0.0.0.0 --port 8000