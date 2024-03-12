# app/management/commands/parse_links.py

from django.core.management.base import BaseCommand
from app.management.scripts.link_parse import fetch_and_parse  # Предположим, что ваша функция fetch_and_parse находится здесь


class Command(BaseCommand):
    help = 'Parse links from a website and save them to a file.'

    def handle(self, *args, **kwargs):
        base_url = "https://www.bonanza.com/booths/show_page/Joy_Styles.html?item_sort_options%5Bpage%5D={}&userRecaptchaResponse=null"
        links_file = "app/management/scripts/unique_links.txt"

        with open(links_file, 'w', encoding='utf-8') as file:
            for page_number in range(1, 6):  # Адаптируйте диапазон по вашему усмотрению
                current_url = base_url.format(page_number)
                self.stdout.write(f"Processing page {page_number}: {current_url}")
                links = fetch_and_parse(current_url, page_number)
                for link in links:
                    file.write(f'{link}\n')

        self.stdout.write(self.style.SUCCESS('Successfully parsed links.'))
