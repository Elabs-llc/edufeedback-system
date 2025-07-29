from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.contrib.auth.models import User
from django.db import connection, transaction
import os


class Command(BaseCommand):
    help = 'Set up production environment - run migrations and create superuser'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🚀 Starting production setup...'))
        
        # Ensure database is ready
        self.ensure_database_ready()
        
        # Create superuser if it doesn't exist
        self.create_superuser()
        
        # Create demo data if needed
        self.create_demo_data()
        
        self.stdout.write(self.style.SUCCESS('\n🎉 Production setup completed!'))
        self.stdout.write(self.style.SUCCESS('🌐 Your EduFeedback System is ready to use!'))
        self.stdout.write(self.style.WARNING('🔐 Default admin login: admin/admin123'))
        self.stdout.write(self.style.ERROR('⚠️  SECURITY: Change admin password immediately!'))

    def ensure_database_ready(self):
        """Ensure database connection and tables exist"""
        self.stdout.write(self.style.WARNING('🔍 Checking database...'))
        
        max_retries = 3
        for attempt in range(max_retries):
            try:
                with connection.cursor() as cursor:
                    # Check if User table exists
                    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='auth_user';")
                    result = cursor.fetchone()
                    
                    if result:
                        self.stdout.write(self.style.SUCCESS('✅ Database tables exist'))
                        return True
                    else:
                        self.stdout.write(self.style.WARNING(f'⚠️  User table not found, running migrations (attempt {attempt + 1})'))
                        call_command('migrate', verbosity=2, interactive=False)
                        
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'⚠️  Database check failed (attempt {attempt + 1}): {e}'))
                if attempt < max_retries - 1:
                    self.stdout.write(self.style.WARNING('🔄 Retrying...'))
                    try:
                        call_command('migrate', verbosity=2, interactive=False)
                    except Exception as migrate_error:
                        self.stdout.write(self.style.ERROR(f'Migration failed: {migrate_error}'))
                else:
                    raise e
        
        return True

    def create_superuser(self):
        """Create superuser with error handling"""
        try:
            if not User.objects.filter(is_superuser=True).exists():
                self.stdout.write(self.style.WARNING('👤 Creating default superuser...'))
                
                with transaction.atomic():
                    user = User.objects.create_superuser(
                        username='admin',
                        email='admin@edufeedback.com',
                        password='admin123',
                        first_name='System',
                        last_name='Administrator'
                    )
                    self.stdout.write(self.style.SUCCESS(f'✅ Superuser created: {user.username}/admin123'))
                    self.stdout.write(self.style.WARNING('⚠️  IMPORTANT: Change password after first login!'))
            else:
                admin_users = User.objects.filter(is_superuser=True)
                self.stdout.write(self.style.WARNING(f'👤 {admin_users.count()} superuser(s) already exist'))
                for admin in admin_users:
                    self.stdout.write(f'   - {admin.username} ({admin.email})')
                    
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Superuser creation failed: {e}'))
            # Create a basic admin user as fallback
            try:
                self.stdout.write(self.style.WARNING('🔄 Trying fallback user creation...'))
                User.objects.create_user(
                    username='admin',
                    email='admin@edufeedback.com',
                    password='admin123',
                    is_staff=True,
                    is_superuser=True
                )
                self.stdout.write(self.style.SUCCESS('✅ Fallback superuser created'))
            except Exception as fallback_error:
                self.stdout.write(self.style.ERROR(f'❌ Fallback creation also failed: {fallback_error}'))

    def create_demo_data(self):
        """Create demo data if needed"""
        try:
            self.stdout.write(self.style.WARNING('� Setting up demo data...'))
            call_command('setup_demo_data', '--create-lecturers', '--create-courses')
            self.stdout.write(self.style.SUCCESS('✅ Demo data created'))
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'⚠️  Demo data setup failed (this is okay): {e}'))
