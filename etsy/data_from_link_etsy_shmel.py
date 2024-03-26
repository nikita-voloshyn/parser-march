import os
import json
import random
import re
import datetime
import uuid

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import asyncio
from concurrent.futures import ThreadPoolExecutor

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
]


def get_random_user_agent():
    return random.choice(user_agents)


def load_proxies(file_path):
    with open(file_path, 'r') as f:
        proxies = f.read().splitlines()
    return proxies


def load_cookies_from_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        cookies = json.load(file)
    return cookies


def set_cookies(driver, cookies):
    for cookie in cookies:
        driver.add_cookie(cookie)

def parse_size(size_string):
    parts = size_string.split()
    if len(parts) >= 1 and size_string != "Select an option":
        size = float(parts[0])
        width = None
        if len(parts) >= 2:
            if parts[1].isalpha():
                width = parts[1]
            if len(parts) >= 3 and parts[2].isalpha():
                width = parts[2]
        return {'size': size, 'width': width}
    return None

def fetch_and_parse(url, cookies, proxies):
    results = {'url': url, 'sizes': [], 'price': 0, 'name': '', 'item_detail': ''}

    random_user_agent = get_random_user_agent()

    # Use random user agent
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--lang=en-US")
    chrome_options.add_argument("--disable-cache")
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_argument("--referer=https://www.etsy.com/shop/chmelgroup")
    chrome_options.add_argument(f"user-agent={random_user_agent}")

    while proxies:
        proxy = proxies.pop(0)
        print(f"Using proxy: {proxy}")

        # Fetch data and parse
        with webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options) as driver:
            driver.get(url)
            driver.set_page_load_timeout(5)  # Set a timeout for page loading

            try:
                product_name_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="listing-page-cart"]/div[4]/h1'))
                )
                name = product_name_element.text.strip()
                results['name'] = name
            except TimeoutException:
                print(f"Proxy {proxy} timed out. Removing from the list.")
                continue
            except:
                results['name'] = "Name not found"

            try:
                item_detail_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located(
                        (By.XPATH, '//*[@id="wt-content-toggle-product-details-read-more"]/p'))
                )
                item_detail = item_detail_element.text.strip()
                results['item_detail'] = item_detail
            except:
                results['item_detail'] = "Item detail not found"

            try:
                price = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="listing-page-cart"]/div[2]/div/div/div/p'))
                )
                price_element = price.text
                price_match = re.search(r'\d+\.\d+', price_element)
                if price_match:
                    results['price'] = float(price_match.group(0))
                else:
                    results['price'] = "Price not found"
            except:
                results['price'] = "Price not found"

            try:
                size_options = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="variation-selector-1"]'))
                )
                sizes_text = size_options.text.strip()
                sizes = sizes_text.split('\n')
                for size in sizes:
                    if size != "Select a size":
                        results['sizes'].append(parse_size(size))
            except:
                try:
                    size_options = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, '//*[@id="variation-selector-0"]'))
                    )
                    sizes_text = size_options.text.strip()
                    sizes = sizes_text.split('\n')
                    for size in sizes:
                        if size != "Select a size":
                            results['sizes'].append(parse_size(size))
                except:
                    results['sizes'] = "Sizes not found"

            # If request succeeds, break out of the loop
            print(f"Successfully fetched data for URL: {url}")  # Added print
            break

    return results


def read_links_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        return data


def current_datetime():
    return datetime.datetime.now().isoformat()

def generate_unique_key(prefix):
    return f"{prefix}_{uuid.uuid4().hex[:9]}"  # Получаем первые 9 символов идентификатора UUID



async def fetch_multiple(urls, cookies, proxies):
    results = []  # Создаем список результатов

    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor(max_workers=15) as executor:
        tasks = [
            loop.run_in_executor(executor, fetch_and_parse, url, cookies, proxies)
            for url in urls
        ]
        for result in await asyncio.gather(*tasks):
            # Генерируем уникальный ключ для каждого товара
            prefix = "BB0" if "bootbarn.com" in result['url'] else "ET0"
            result['unique_key'] = generate_unique_key(prefix)

            # Добавляем поля с датой создания и датой обновления в результаты
            result['created_at'] = current_datetime()
            result['updated_at'] = current_datetime()

            results.append(result)  # Добавляем результаты в список

    return results


async def main_async():
    links_file = "unique_links_shmel.json"
    cookies_file = "cookies_etsy.json"
    proxies_file = "proxies.txt"

    if not os.path.exists(cookies_file):
        print("File with cookies not found.")
        return

    cookies = load_cookies_from_json(cookies_file)

    if not os.path.exists(proxies_file):
        print("File with proxies not found.")
        return

    proxies = load_proxies(proxies_file)

    links = read_links_from_file(links_file)
    results = await fetch_multiple(links, cookies, proxies)

    # Создаем список для всех результатов
    all_results = []

    for result in results:
        # Добавляем результаты в список
        all_results.append(result)

    # Записываем все результаты в файл как один JSON-объект
    output_file = "output_chmelgroup.json"
    with open(output_file, 'w') as f:
        json.dump(all_results, f, indent=4)


if __name__ == "__main__":
    asyncio.run(main_async())
# //*[@id="variation-selector-1"]