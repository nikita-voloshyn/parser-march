# app/management/commands/fetch_data.py

from django.core.management.base import BaseCommand
from app.management.scripts.data_from_link import fetch_and_parse, read_links_from_file, load_cache
import json

class Command(BaseCommand):
    help = 'Fetch data from URLs and update the cache.'

    def handle(self, *args, **options):
        links_file = "app/management/scripts/unique_links.txt"
        cache_file = "cache.db"

        links = read_links_from_file(links_file)
        cache = load_cache(cache_file)

        results = []  # Define results list here

        for url in links:
            self.stdout.write(f"Processing: {url}")
            result = fetch_and_parse(url, cache)
            results.append(result)  # Append the result to the results list

        # Ensure you have logic inside fetch_and_parse to update the cache if necessary

        # Save the results to a JSON file
        with open("app/management/scripts/parsed_data.json", 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=4)

        self.stdout.write(self.style.SUCCESS('Successfully fetched data for all URLs.'))
