#!/bin/bash

# Kill the frontend
sudo pkill -f "serve -s build -p 80"

# Kill the backend
sudo pkill -f "python -m presstagram_backend"
