from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.contrib.auth.models import User
from django.db import connection
import os


class Command(BaseCommand):
    help = 'Set up production environment - run migrations and create superuser'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🚀 Starting production setup...'))
        
        # Check if database exists and is accessible
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
            self.stdout.write(self.style.SUCCESS('✅ Database connection successful'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Database connection failed: {e}'))
            return
        
        # Run migrations
        self.stdout.write(self.style.WARNING('🔄 Running database migrations...'))
        try:
            call_command('migrate', verbosity=1, interactive=False)
            self.stdout.write(self.style.SUCCESS('✅ Migrations completed'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Migration failed: {e}'))
            return
        
        # Create superuser if it doesn't exist
        if not User.objects.filter(is_superuser=True).exists():
            self.stdout.write(self.style.WARNING('👤 Creating default superuser...'))
            try:
                User.objects.create_superuser(
                    username='admin',
                    email='admin@edufeedback.com',
                    password='admin123',
                    first_name='System',
                    last_name='Administrator'
                )
                self.stdout.write(self.style.SUCCESS('✅ Superuser created: admin/admin123'))
                self.stdout.write(self.style.WARNING('⚠️  IMPORTANT: Change password after first login!'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'❌ Superuser creation failed: {e}'))
        else:
            self.stdout.write(self.style.WARNING('👤 Superuser already exists, skipping...'))
        
        # Collect static files
        self.stdout.write(self.style.WARNING('📁 Collecting static files...'))
        try:
            call_command('collectstatic', verbosity=1, interactive=False)
            self.stdout.write(self.style.SUCCESS('✅ Static files collected'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Static files collection failed: {e}'))
        
        # Create demo data if needed
        self.stdout.write(self.style.WARNING('🎭 Setting up demo data...'))
        try:
            call_command('setup_demo_data', '--create-lecturers', '--create-courses')
            self.stdout.write(self.style.SUCCESS('✅ Demo data created'))
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'⚠️  Demo data setup failed (this is okay): {e}'))
        
        self.stdout.write(self.style.SUCCESS('\n🎉 Production setup completed!'))
        self.stdout.write(self.style.SUCCESS('🌐 Your EduFeedback System is ready to use!'))
        self.stdout.write(self.style.WARNING('🔐 Default admin login: admin/admin123'))
        self.stdout.write(self.style.ERROR('⚠️  SECURITY: Change admin password immediately!'))
