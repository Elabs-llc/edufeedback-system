#!/usr/bin/env bash
# Exit on error
set -o errexit

echo "🚀 Starting build process..."

# Install system dependencies for psycopg2
apt-get update && apt-get install -y libpq-dev python3-dev

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# for debugging
echo "🐍 Pip freeze..."
pip freeze

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

# Apply database migrations
echo "🗄️ Applying database migrations..."
python manage.py migrate

# Create superuser from environment variables
# This is safe because the script will only run once on build
echo "👤 Creating or updating admin user..."
python -c "
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'feedback_system.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

username = os.getenv('DJANGO_SUPERUSER_USERNAME', 'admin')
email = os.getenv('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
password = os.getenv('DJANGO_SUPERUSER_PASSWORD', 'admin123')

if not User.objects.filter(username=username).exists():
    print(f'Creating superuser {username}...')
    User.objects.create_superuser(username, email, password)
    print('✅ Superuser created.')
else:
    print(f'Superuser {username} already exists.')

"

echo "✅ Build finished successfully!"
