import requests
import requests_cache
from bs4 import BeautifulSoup
import json
import re

requests_cache.install_cache('bootbarn_cache', expire_after=300)

def fetch_listings(url):
    unique_ids = set()

    print(f"Обрабатывается: {url}")
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Ошибка при запросе страницы: {response.status_code}")
        return

    if response.from_cache:
        print("Ответ загружен из кеша")
    else:
        print("Ответ получен от сервера и сохранен в кеш")

    html = response.content
    soup = BeautifulSoup(html, 'html.parser')

    listings = soup.find_all('a', href=True)
    for link in listings:
        match = re.search(r'/(\d+)\.html', link['href'])
        if match:
            unique_ids.add(match.group(1))

    with open('unique_links_bootbarn.json', 'w') as json_file:
        formatted_links = [f"https://www.bootbarn.com/{id}.html" for id in unique_ids]
        json.dump(formatted_links, json_file, indent=4)

    print(f"\nВсего найдено уникальных ссылок: {len(unique_ids)}. Сохранено в unique_links.json")

url = 'https://www.bootbarn.com/mens/boots-shoes/mens-boots-shoes/?start=50'
fetch_listings(url)