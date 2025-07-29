from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import connection
import os


class Command(BaseCommand):
    help = 'Initialize database - force create all tables'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🔧 Initializing database...'))
        
        try:
            # Remove existing database
            db_path = 'db.sqlite3'
            if os.path.exists(db_path):
                os.remove(db_path)
                self.stdout.write(self.style.WARNING(f'🗑️ Removed existing database: {db_path}'))
            
            # Run migrations in specific order
            self.stdout.write(self.style.WARNING('🔄 Running core Django migrations...'))
            call_command('migrate', 'contenttypes', verbosity=2, interactive=False)
            call_command('migrate', 'auth', verbosity=2, interactive=False)
            call_command('migrate', 'admin', verbosity=2, interactive=False)
            call_command('migrate', 'sessions', verbosity=2, interactive=False)
            
            # Run our app migrations
            self.stdout.write(self.style.WARNING('🔄 Running feedback app migrations...'))
            call_command('migrate', 'feedback', verbosity=2, interactive=False)
            
            # Run any remaining migrations
            self.stdout.write(self.style.WARNING('🔄 Running any remaining migrations...'))
            call_command('migrate', verbosity=2, interactive=False)
            
            # Verify tables exist
            with connection.cursor() as cursor:
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = [row[0] for row in cursor.fetchall()]
                self.stdout.write(self.style.SUCCESS(f'✅ Created {len(tables)} tables:'))
                for table in sorted(tables):
                    self.stdout.write(f'   - {table}')
            
            self.stdout.write(self.style.SUCCESS('🎉 Database initialization completed!'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Database initialization failed: {e}'))
            raise e
