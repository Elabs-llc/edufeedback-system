#!/usr/bin/env python
"""
Debug script to test login functionality
Run this after deployment to check what's causing the 500 error
"""

import os
import django
from django.conf import settings

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'feedback_system.settings')
django.setup()

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse

def test_database():
    print("🔍 Testing database connection...")
    try:
        users = User.objects.all()
        print(f"✅ Database connected. Found {users.count()} users.")
        
        # Check if admin user exists
        admin_users = User.objects.filter(is_superuser=True)
        print(f"👤 Found {admin_users.count()} admin users:")
        for admin in admin_users:
            print(f"   - {admin.username} ({admin.email})")
        
        return True
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

def test_authentication():
    print("\n🔐 Testing authentication...")
    try:
        # Try to authenticate with default admin
        user = authenticate(username='admin', password='admin123')
        if user:
            print(f"✅ Authentication successful for: {user.username}")
            print(f"   - Is active: {user.is_active}")
            print(f"   - Is superuser: {user.is_superuser}")
            return True
        else:
            print("❌ Authentication failed with admin/admin123")
            return False
    except Exception as e:
        print(f"❌ Authentication error: {e}")
        return False

def test_login_view():
    print("\n🌐 Testing login view...")
    try:
        client = Client()
        
        # Test GET request to login page
        response = client.get('/login/')
        print(f"GET /login/ - Status: {response.status_code}")
        
        # Test POST request with credentials
        response = client.post('/login/', {
            'username': 'admin',
            'password': 'admin123'
        })
        print(f"POST /login/ - Status: {response.status_code}")
        
        if response.status_code == 302:
            print(f"✅ Login successful - redirected to: {response.get('Location', 'unknown')}")
            return True
        else:
            print(f"❌ Login failed - Status: {response.status_code}")
            if hasattr(response, 'content'):
                print(f"Response content: {response.content[:200]}...")
            return False
            
    except Exception as e:
        print(f"❌ Login view error: {e}")
        return False

def main():
    print("🚀 EduFeedback System Login Debug")
    print("=" * 40)
    
    # Test database
    db_ok = test_database()
    
    # Test authentication
    auth_ok = test_authentication()
    
    # Test login view
    view_ok = test_login_view()
    
    print("\n" + "=" * 40)
    print("📊 Summary:")
    print(f"Database: {'✅' if db_ok else '❌'}")
    print(f"Authentication: {'✅' if auth_ok else '❌'}")
    print(f"Login View: {'✅' if view_ok else '❌'}")
    
    if all([db_ok, auth_ok, view_ok]):
        print("\n🎉 All tests passed! Login should work.")
    else:
        print("\n⚠️  Some tests failed. Check the errors above.")

if __name__ == '__main__':
    main()
