#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

echo "=== Installing konfiva ==="

if ! command -v python3 &> /dev/null; then
    echo "Python 3 is required. Install from https://python.org/"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d venv ]; then
    python3 -m venv venv
fi

./venv/bin/pip install --upgrade pip
./venv/bin/pip install -r requirements.txt

if [ ! -f .env ]; then
    cp .env.example .env
    echo "Created .env from .env.example. Set SECRET_KEY and other values before production use."
fi

# Ensure persistence directories exist
mkdir -p instance config configs

echo ""
echo "konfiva installed. Start it with:"
echo "  ./venv/bin/python app.py"
echo ""
echo "Or use Docker:"
echo "  docker compose up -d"
