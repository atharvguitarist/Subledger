#!/usr/bin/env bash
set -e

if [ ! -d .venv ]; then
  python3 -m venv .venv
fi

. .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

if [ ! -f .env ]; then
  cp .env.example .env
fi

uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
