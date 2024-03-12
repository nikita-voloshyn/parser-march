from django.core.management.base import BaseCommand
from app.management.scripts.link_parse import fetch_listings

class Command(BaseCommand):
    help = 'Fetch listings from a specified URL and save unique links to a JSON file'

    def add_arguments(self, parser):
        parser.add_argument('https://www.bootbarn.com/mens/boots-shoes/mens-boots-shoes/?start=50', type=str, help='URL to fetch listings from')

    def handle(self, *args, **options):
        url = options['url']
        fetch_listings(url)
        self.stdout.write(self.style.SUCCESS('Successfully fetched listings.'))
