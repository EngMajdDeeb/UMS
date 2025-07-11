#!/usr/bin/env python3
import os
import sys
import django
from django.contrib.auth.models import User

# Add the project path to the Python path
sys.path.insert(0, '/app')

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'university_erp.settings')
django.setup()

# Create superuser
username = 'admin'
email = 'admin@university.edu'
password = 'admin123'

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f"✅ Superuser created: {username}")
    print(f"   Email: {email}")
    print(f"   Password: {password}")
else:
    print(f"⚠️  Superuser {username} already exists")

print("\n🎉 Setup complete! You can now login with the above credentials.")