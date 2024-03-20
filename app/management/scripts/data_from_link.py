import os
import json
import random
import re
import asyncio
from concurrent.futures import ThreadPoolExecutor

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager

# Список user-agent'ов
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

# Функция для получения случайного user-agent'а
def get_random_user_agent():
    return random.choice(user_agents)

# Функция для загрузки списка прокси из файла
def load_proxies(file_path):
    with open(file_path, 'r') as f:
        proxies = f.read().splitlines()
    return proxies

# Функция для загрузки cookies из JSON файла
def load_cookies_from_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        cookies = json.load(file)
    return cookies

# Функция для установки cookies в браузер
def set_cookies(driver, cookies):
    for cookie in cookies:
        driver.add_cookie(cookie)

# Функция для загрузки и парсинга данных
def fetch_and_parse(url, cookies, proxies):
    results = {'url': url, 'sizes': [], 'price': 0, 'name': '', 'item_detail': ''}

    random_user_agent = get_random_user_agent()

    # Use random user agent
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--lang=en-US")
    chrome_options.add_argument("--disable-cache")
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_argument("--referer=https://www.bootbarn.com/mens/boots-shoes/mens-boots-shoes/?start=50")
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
                    EC.presence_of_element_located((By.XPATH, '//*[@id="pdpMain"]/header/div/h1'))
                )
                name = product_name_element.text.strip()
                results['name'] = name
            except TimeoutException:
                print(f"Proxy {proxy} timed out. Removing from the list.")
                continue
            except:
                results['name'] = "Name not found"

            try:
                price_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located(
                        (By.XPATH, '//*[@id="pdpMain"]/div[2]/div[2]/div[1]/div/span[1]/strong'))
                )
                price_text = price_element.text.strip()
                price_match = re.search(r'(\d+\.\d+)', price_text)
                if price_match:
                    price = float(price_match.group(1))
                    results['price'] = price
                else:
                    results['price'] = "Price not found"
            except:
                results['price'] = "Price not found"



            print(f"Successfully fetched data for URL: {url}")  # Added print
            break
    # Saving result to file
    output_file = "output.json"
    with open(output_file, 'a') as f:
        json.dump(results, f, indent=4)
        f.write('\n')

    return results


def read_links_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        return data


async def fetch_multiple(urls, cookies, proxies):
    results = []  # Создаем список результатов

    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor(max_workers=15) as executor:
        tasks = [
            loop.run_in_executor(executor, fetch_and_parse, url, cookies, proxies)
            for url in urls
        ]
        for result in await asyncio.gather(*tasks):
            results.append(result)  # Добавляем результаты в список

    return results


async def main_async():
    links_file = "unique_links.json"
    cookies_file = "cookies.json"
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
    await fetch_multiple(links, cookies, proxies)


if __name__ == "__main__":
    asyncio.run(main_async())