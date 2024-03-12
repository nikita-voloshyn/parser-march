import os
import shelve
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36")

def load_cache(cache_path):
    if os.path.exists(cache_path):
        with shelve.open(cache_path, flag='r') as cache:
            return dict(cache)
    return {}

def save_to_cache(cache_path, url, data):
    with shelve.open(cache_path, writeback=True) as cache:
        cache[url] = data

def fetch_and_parse(url, cache):
    if url in cache:
        return cache[url]

    results = {'url': url}
    with webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options) as driver:
        driver.get(url)

        # Извлечение названия товара
        try:
            product_name_element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="content"]/div[1]/div[3]/div/div[2]/div[1]/h2/span'))
            )
            name = product_name_element.text.strip()
            results['name'] = name
        except:
            results['name'] = "Название товара не найдено"

        # Извлечение размеров товара
        try:
            size_options = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, '//*[@id="item_to_add_item_trait_mutation_id"]/option'))
            )
            sizes = [option.text.strip() for option in size_options if option.get_attribute('value') != '0']
            results['sizes'] = sizes
        except:
            results['sizes'] = "Размеры не найдены"

        # Сохраняем результаты в кеш
        save_to_cache('cache.db', url, results)

    return results

def read_links_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file.readlines()]

def main():
    links_file = "unique_links.txt"
    cache_file = "cache.db"

    links = read_links_from_file(links_file)
    cache = load_cache(cache_file)

    for url in links:
        print(f"Processing: {url}")
        result = fetch_and_parse(url, cache)

if __name__ == "__main__":
    main()
