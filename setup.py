#!/usr/bin/env python
"""
Setup script for Django Feedback System
This script automates the initial setup process
"""

import os
import sys
import subprocess
import platform

def run_command(command, description):
    """Run a system command and handle errors"""
    print(f"\n{'='*50}")
    print(f"Running: {description}")
    print(f"Command: {command}")
    print(f"{'='*50}")
    
    try:
        if platform.system() == "Windows":
            result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        else:
            result = subprocess.run(command.split(), check=True, capture_output=True, text=True)
        
        print("✅ Success!")
        if result.stdout:
            print(f"Output: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        if e.stdout:
            print(f"Output: {e.stdout}")
        if e.stderr:
            print(f"Error: {e.stderr}")
        return False

def setup_feedback_system():
    """Main setup function"""
    print("🚀 Django Feedback System Setup")
    print("This script will set up your feedback system automatically.\n")
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required!")
        return False
    
    print(f"✅ Python {sys.version} detected")
    
    # Install dependencies
    if not run_command("pip install -r requirements.txt", "Installing Python dependencies"):
        print("⚠️  Failed to install dependencies. Please run 'pip install -r requirements.txt' manually.")
        return False
    
    # Create migrations
    if not run_command("python manage.py makemigrations", "Creating database migrations"):
        print("⚠️  Failed to create migrations.")
        return False
    
    # Apply migrations
    if not run_command("python manage.py migrate", "Applying database migrations"):
        print("⚠️  Failed to apply migrations.")
        return False
    
    # Collect static files
    if not run_command("python manage.py collectstatic --noinput", "Collecting static files"):
        print("⚠️  Failed to collect static files.")
    
    print("\n" + "="*60)
    print("🎉 SETUP COMPLETE!")
    print("="*60)
    print("\nNext steps:")
    print("1. Create a superuser: python manage.py createsuperuser")
    print("2. Start the server: python manage.py runserver")
    print("3. Open http://127.0.0.1:8000/ in your browser")
    print("\nFor production deployment, see README.md")
    
    # Ask if user wants to create superuser
    create_superuser = input("\nWould you like to create a superuser now? (y/n): ").lower().strip()
    if create_superuser in ['y', 'yes']:
        run_command("python manage.py createsuperuser", "Creating superuser")
    
    # Ask if user wants to start server
    start_server = input("\nWould you like to start the development server now? (y/n): ").lower().strip()
    if start_server in ['y', 'yes']:
        print("\n🌐 Starting development server...")
        print("Server will be available at: http://127.0.0.1:8000/")
        print("Admin panel at: http://127.0.0.1:8000/admin/")
        print("\nPress Ctrl+C to stop the server")
        
        try:
            subprocess.run("python manage.py runserver", shell=True, check=True)
        except KeyboardInterrupt:
            print("\n\n👋 Server stopped. Thank you for using Django Feedback System!")
        except subprocess.CalledProcessError as e:
            print(f"\n❌ Failed to start server: {e}")
    
    return True

if __name__ == "__main__":
    if not setup_feedback_system():
        sys.exit(1)
