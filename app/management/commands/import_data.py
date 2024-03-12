# your_app/management/commands/import_data.py

from django.core.management.base import BaseCommand
from app.models import Product
import json

class Command(BaseCommand):
    help = 'Import data from JSON file into the database.'

    def handle(self, *args, **kwargs):
        with open('app/management/scripts/parsed_data.json', 'r') as file:
            data = json.load(file)
            for item in data:
                Product.objects.update_or_create(
                    url=item['url'],
                    defaults=item
                )
        self.stdout.write(self.style.SUCCESS('Successfully imported data into the database.'))
