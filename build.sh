#!/usr/bin/env bash
# Render build script for EduFeedback System

set -o errexit  # Exit on any error

echo "🚀 Starting build process..."

# Install Python dependencies
echo "📦 Installing Python packages..."
pip install --upgrade pip
pip install -r requirements.txt

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

# Run production setup (migrations, superuser, demo data)
echo "🔧 Setting up production environment..."
python manage.py setup_production

echo "✅ Build completed successfully!"
