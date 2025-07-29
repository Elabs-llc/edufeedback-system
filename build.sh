#!/usr/bin/env bash
# Exit on error
set -o errexit

echo "🚀 Starting build process..."

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

# Initialize database with our custom command
echo "🗄️ Initializing database..."
python manage.py init_database

# Create superuser and setup production data
echo "👤 Setting up production environment..."
python manage.py setup_production

echo "✅ Build completed successfully!"
