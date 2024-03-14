import requests
from bs4 import BeautifulSoup
import json
import time

def fetch_listings(base_url, start_page=1):
    page = start_page
    unique_links = set()  # Множество для хранения уникальных ссылок

    while True:
        url = f'{base_url}?page={page}#items'
        print(f"Обрабатывается: {url}")

        # Создание заголовков для имитации поведения браузера
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
        }

        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Ошибка при запросе страницы: {response.status_code}")
            break

        html = response.content
        time.sleep(3)  # Задержка в 3 секунды между запросами
        soup = BeautifulSoup(html, 'html.parser')

        # Извлечение ссылок на товары
        listings = soup.find_all('a', href=True)
        page_links = [link['href'].split('?')[0] for link in listings if '/listing/' in link['href']]

        # Поиск новых уникальных ссылок
        new_links = set(page_links) - unique_links
        if not new_links:
            print("Новые уникальные товары не найдены на странице. Завершение работы.")
            break

        unique_links.update(new_links)
        page += 1

    # Сохранение уникальных ссылок в JSON-файл
    with open('unique_links.json', 'w') as json_file:
        json.dump(list(unique_links), json_file, indent=4)

    print(f"\nВсего найдено уникальных ссылок: {len(unique_links)}. Сохранено в unique_links.json")


# Базовый URL магазина без параметра страницы
base_url = 'https://www.etsy.com/shop/BirdTeesUS'
fetch_listings(base_url)
