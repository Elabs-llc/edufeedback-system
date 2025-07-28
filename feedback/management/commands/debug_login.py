from django.core.management.base import BaseCommand
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.test import Client


class Command(BaseCommand):
    help = 'Debug login functionality'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🚀 EduFeedback Login Debug'))
        self.stdout.write('=' * 40)
        
        # Test database
        self.test_database()
        
        # Test authentication
        self.test_authentication()
        
        # Test login view
        self.test_login_view()

    def test_database(self):
        self.stdout.write(self.style.WARNING('🔍 Testing database connection...'))
        try:
            users = User.objects.all()
            self.stdout.write(self.style.SUCCESS(f'✅ Database connected. Found {users.count()} users.'))
            
            # Check if admin user exists
            admin_users = User.objects.filter(is_superuser=True)
            self.stdout.write(self.style.SUCCESS(f'👤 Found {admin_users.count()} admin users:'))
            for admin in admin_users:
                self.stdout.write(f'   - {admin.username} ({admin.email})')
            
            return True
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Database error: {e}'))
            return False

    def test_authentication(self):
        self.stdout.write(self.style.WARNING('\n🔐 Testing authentication...'))
        try:
            # Try to authenticate with default admin
            user = authenticate(username='admin', password='admin123')
            if user:
                self.stdout.write(self.style.SUCCESS(f'✅ Authentication successful for: {user.username}'))
                self.stdout.write(f'   - Is active: {user.is_active}')
                self.stdout.write(f'   - Is superuser: {user.is_superuser}')
                return True
            else:
                self.stdout.write(self.style.ERROR('❌ Authentication failed with admin/admin123'))
                return False
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Authentication error: {e}'))
            return False

    def test_login_view(self):
        self.stdout.write(self.style.WARNING('\n🌐 Testing login view...'))
        try:
            client = Client()
            
            # Test GET request to login page
            response = client.get('/login/')
            self.stdout.write(f'GET /login/ - Status: {response.status_code}')
            
            # Test POST request with credentials
            response = client.post('/login/', {
                'username': 'admin',
                'password': 'admin123'
            })
            self.stdout.write(f'POST /login/ - Status: {response.status_code}')
            
            if response.status_code == 302:
                self.stdout.write(self.style.SUCCESS(f'✅ Login successful - redirected to: {response.get("Location", "unknown")}'))
                return True
            else:
                self.stdout.write(self.style.ERROR(f'❌ Login failed - Status: {response.status_code}'))
                return False
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Login view error: {e}'))
            return False
