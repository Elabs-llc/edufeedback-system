#!/usr/bin/env bash
# Render build script

# Install system dependencies
apt-get update
apt-get install -y libpq-dev

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput
