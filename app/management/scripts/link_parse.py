import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import re
import os

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36")

def fetch_and_parse(url, page_number):
    # Инициализация драйвера
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    # Путь к файлу кеша
    cache_file = f"cache_page_{page_number}.html"

    if not os.path.exists(cache_file):
        driver.get(url)
        time.sleep(3)

        # Сохранение страницы в файл кеша
        with open(cache_file, 'w', encoding='utf-8') as file:
            file.write(driver.page_source)

        driver.quit()

    with open(cache_file, 'r', encoding='utf-8') as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, 'html.parser')

    # Извлечение ссылок
    pattern = re.compile(r'/listings/.+?/(\d+)')
    unique_links = set()
    for a in soup.find_all('a', href=True):
        match = pattern.search(a['href'])
        if match:
            unique_id = match.group(1)
            link = f"https://www.bonanza.com/listings/{unique_id}"
            unique_links.add(link)

    return unique_links


# Файл для сохранения результатов
links_file = "unique_links.txt"

with open(links_file, 'w', encoding='utf-8') as file:
    base_url = "https://www.bonanza.com/booths/show_page/Joy_Styles.html?item_sort_options%5Bpage%5D={}&userRecaptchaResponse=null"

    for page_number in range(1, 6):  # Пример диапазона страниц
        current_url = base_url.format(page_number)
        print(f"Processing page {page_number}: {current_url}")
        links = fetch_and_parse(current_url, page_number)
        for link in links:
            file.write(link + "\n")
