from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site

class Command(BaseCommand):
    help = 'Create default site entry for Django Sites framework'

    def handle(self, *args, **options):
        try:
            # Try to create the default site
            site, created = Site.objects.get_or_create(
                id=1,
                defaults={'domain': 'localhost:8000', 'name': 'OctoFit Tracker'}
            )
            if created:
                self.stdout.write(self.style.SUCCESS('Successfully created default site'))
            else:
                self.stdout.write(self.style.SUCCESS('Default site already exists'))
        except Exception as e:
            # If there's an error, manually insert using MongoDB
            from pymongo import MongoClient
            client = MongoClient('localhost', 27017)
            db = client['octofit_tracker']
            
            existing = db.django_site.find_one({'_id': 1})
            if not existing:
                db.django_site.insert_one({
                    '_id': 1,
                    'id': 1,
                    'domain': 'localhost:8000',
                    'name': 'OctoFit Tracker'
                })
                self.stdout.write(self.style.SUCCESS('Successfully created site via MongoDB'))
            else:
                self.stdout.write(self.style.SUCCESS('Site already exists in MongoDB'))
