# app/management/commands/parse_links.py
from django.core.management.base import BaseCommand
from app.management.scripts import bf  # Импортируйте ваш модуль bf

class Command(BaseCommand):
    help = 'Parse links from the specified URL'

    def add_arguments(self, parser):
        parser.add_argument('url', type=str, help='The URL to parse links from')

    def handle(self, *args, **options):
        url = options['url']
        bf.fetch_listings(url)  # Предполагается, что это ваша функция для парсинга
        self.stdout.write(self.style.SUCCESS(f'Successfully parsed links from {url}'))
