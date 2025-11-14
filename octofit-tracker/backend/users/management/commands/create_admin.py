from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from pymongo import MongoClient
from django.contrib.auth.hashers import make_password
import datetime

class Command(BaseCommand):
    help = 'Create superuser using direct MongoDB insertion'

    def handle(self, *args, **options):
        try:
            # Try Django ORM first
            if not User.objects.filter(username='admin').exists():
                user = User.objects.create_superuser(
                    username='admin',
                    email='admin@octofit.com',
                    password='admin123'
                )
                self.stdout.write(self.style.SUCCESS('Superuser created via Django ORM'))
                
                # Create associated profile
                from users.models import UserProfile
                UserProfile.objects.get_or_create(user=user)
                self.stdout.write(self.style.SUCCESS('User profile created'))
            else:
                self.stdout.write(self.style.WARNING('Superuser already exists'))
        except Exception as e:
            # Fallback to direct MongoDB insertion
            self.stdout.write(self.style.WARNING(f'Django ORM failed: {e}'))
            self.stdout.write(self.style.WARNING('Attempting direct MongoDB insertion...'))
            
            client = MongoClient('localhost', 27017)
            db = client['octofit_tracker']
            
            # Check if admin user exists
            existing = db.auth_user.find_one({'username': 'admin'})
            if not existing:
                # Create admin user directly in MongoDB
                hashed_password = make_password('admin123')
                user_doc = {
                    'password': hashed_password,
                    'last_login': None,
                    'is_superuser': True,
                    'username': 'admin',
                    'first_name': '',
                    'last_name': '',
                    'email': 'admin@octofit.com',
                    'is_staff': True,
                    'is_active': True,
                    'date_joined': datetime.datetime.now()
                }
                result = db.auth_user.insert_one(user_doc)
                user_id = result.inserted_id
                
                # Create user profile
                profile_doc = {
                    'user_id': user_id,
                    'bio': '',
                    'age': None,
                    'fitness_level': 'beginner',
                    'height': None,
                    'weight': None,
                    'total_points': 0,
                    'created_at': datetime.datetime.now(),
                    'updated_at': datetime.datetime.now()
                }
                db.user_profiles.insert_one(profile_doc)
                
                self.stdout.write(self.style.SUCCESS('Superuser created via MongoDB'))
                self.stdout.write(self.style.SUCCESS('Username: admin'))
                self.stdout.write(self.style.SUCCESS('Password: admin123'))
            else:
                self.stdout.write(self.style.WARNING('Superuser already exists in MongoDB'))
