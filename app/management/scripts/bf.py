import requests
from bs4 import BeautifulSoup
import json
import time

def fetch_listings(base_url, start_page=1, max_pages=10):
    page = start_page
    unique_links = set()
    processed_pages = 0

    while processed_pages < max_pages:
        url = f'{base_url}?page={page}#items'
        print(f"Обрабатывается: {url}")

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'referer': 'https://www.etsy.com'
        }

        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Ошибка при запросе страницы: {response.status_code}")
            break

        html = response.content
        time.sleep(3)
        soup = BeautifulSoup(html, 'html.parser')

        listings = soup.find_all('a', href=True)
        page_links = [link['href'].split('?')[0] for link in listings if '/listing/' in link['href']]

        new_links = set(page_links) - unique_links
        if not new_links:
            print("Новые уникальные товары не найдены на странице. Завершение работы.")
            break

        unique_links.update(new_links)
        page += 1
        processed_pages += 1

    with open('unique_links.json', 'w') as json_file:
        json.dump(list(unique_links), json_file, indent=4)

    print(f"\nВсего найдено уникальных ссылок: {len(unique_links)}. Сохранено в unique_links.json")

# Пример использования:
fetch_listings("https://www.etsy.com/shop/chmelgroup", start_page=1, max_pages=5)
