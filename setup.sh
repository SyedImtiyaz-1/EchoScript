#!/bin/bash
set -e

echo "=== EchoScript Setup ==="

# System dependencies
echo "[1/5] Installing system dependencies..."
sudo apt-get update -qq
sudo apt-get install -y -qq \
    tesseract-ocr \
    tesseract-ocr-hin tesseract-ocr-ara tesseract-ocr-fra \
    tesseract-ocr-deu tesseract-ocr-spa tesseract-ocr-chi-sim \
    tesseract-ocr-jpn tesseract-ocr-kor \
    ffmpeg

# Python dependencies
echo "[2/5] Installing Python dependencies..."
pip install -r backend/requirements.txt

# Node dependencies
echo "[3/5] Installing frontend dependencies..."
cd frontend && npm install && cd ..

# Create output dir
echo "[4/5] Creating output directory..."
mkdir -p backend/output

# Copy env template
echo "[5/5] Setting up environment..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "Created .env from template. Please edit it with your settings."
else
    echo ".env already exists, skipping."
fi

echo ""
echo "=== Setup Complete ==="
echo "To start the app:"
echo "  Backend:  python -m backend.main"
echo "  Frontend: cd frontend && npm run dev"
