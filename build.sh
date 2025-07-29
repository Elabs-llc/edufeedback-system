#!/usr/bin/env bash
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
echo "�️ Initializing database..."
python manage.py init_database

# Create superuser and setup production data
echo "👤 Setting up production environment..."
python manage.py setup_production

echo "✅ Build completed successfully!" error
set -o errexit

echo "🚀 Starting build process..."

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

# Create database directory if it doesn't exist
mkdir -p /opt/render/project/src

# Remove old database if it exists (fresh start)
rm -f db.sqlite3

# Run migrations with verbose output
echo "� Running database migrations..."
python manage.py makemigrations --verbosity=2
python manage.py migrate --verbosity=2

# Create superuser and setup production data
echo "� Setting up production environment..."
python manage.py setup_production

echo "✅ Build completed successfully!"
