#!/bin/bash

# Ensure deps Python
cat presstagram_backend/requirements.txt | xargs -n 1 python -m pip install

# Ensure deps Node
cd presstagram_frontend
npm install
sudo npm install -g serve

# Build and serve frontend
npm run build
sudo serve -s build -p 80 --cors &

# Run backend
cd ..
python -m presstagram_backend &
