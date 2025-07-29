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

# Simple database setup - Django standard approach
echo "🗄️ Setting up database..."
rm -f db.sqlite3  # Start fresh
python manage.py makemigrations --verbosity=2
python manage.py migrate --verbosity=2

# Create superuser directly using environment variables
echo "👤 Creating admin user..."
python -c "
import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'feedback_system.settings')
django.setup()

from django.contrib.auth.models import User

# Create admin user if not exists
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@edufeedback.com', 'admin123')
    print('✅ Admin user created: admin/admin123')
else:
    print('✅ Admin user already exists')
"

echo "✅ Build completed successfully!"
