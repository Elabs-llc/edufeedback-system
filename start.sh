#!/usr/bin/env bash
# Render start script

echo "🌟 Starting EduFeedback System..."

# Run production setup if needed (idempotent)
python manage.py setup_production --verbosity=0

# Start the application
echo "🚀 Starting Gunicorn server..."
exec gunicorn feedback_system.wsgi:application
