import datetime
import os
import json
import random
import re
import asyncio
import uuid
from concurrent.futures import ThreadPoolExecutor

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager

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
    if len(parts) >= 1:
        size = float(parts[0])
        width = None
        if len(parts) >= 2:
            if parts[1].isalpha():
                width = parts[1]
            elif parts[1] == "1/2":
                size += 0.5
            if len(parts) >= 3 and not width:
                width = parts[2]
        return {'size': size, 'width': width}
    return None


def fetch_and_parse(url, cookies, proxies):
    results = {'url': url, 'sizes': [], 'price': 0, 'name': '', 'item_detail': '', 'color': ''}

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
            driver.set_page_load_timeout(10)

            try:
                product_name_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="pdpMain"]/div[2]/header/div/h1'))
                )
                name = product_name_element.text.strip()
                results['name'] = name
            except TimeoutException:
                print(f"Proxy {proxy} timed out")
                continue
            except:
                results['name'] = "Name not found"

            try:
                international_shipment_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="product-content"]/div[1]/span[2]/div/div'))
                )
                international_shipment = international_shipment_element.text.strip()
                if international_shipment == "OOPS, THIS ITEM IS CURRENTLY UNAVAILABLE FOR INTERNATIONAL SHIPMENT":
                    results['international_shipment'] = False
                else:
                    results['international_shipment'] = True
                    try:
                        size_elements = WebDriverWait(driver, 5).until(
                            EC.presence_of_all_elements_located(
                                (By.XPATH, '//*[@id="product-content"]/div[2]/div/ul/li[2]/div[2]/ul/li/a'))
                        )
                        sizes = [parse_size(size_element.get_attribute("data-size-id")) for size_element in
                                 size_elements]
                        results['sizes'] = sizes
                    except TimeoutException:
                        results['sizes'] = "Sizes not found"

                    try:
                        item_detail_element = WebDriverWait(driver, 5).until(
                            EC.presence_of_element_located(
                                (By.XPATH, '//*[@id="pdpMain"]/div[2]/div[5]/div/div/div/div/ul'))
                        )
                        item_detail = item_detail_element.text.strip()
                        results['item_detail'] = item_detail
                    except:
                        results['item_detail'] = "Item detail not found"

                    try:
                        color_element = WebDriverWait(driver, 5).until(
                            EC.presence_of_element_located(
                                (By.XPATH, '//*[@id="product-content"]/div[2]/div/ul/li[1]/div[1]/span/span[2]'))
                        )
                        color = color_element.text.strip()
                        results['color'] = color
                    except:
                        results['color'] = "Color not found"

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
            except:
                results['international_shipment'] = "International shipment not found"

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
    results = []

    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor(max_workers=15) as executor:
        tasks = [
            loop.run_in_executor(executor, fetch_and_parse, url, cookies, proxies)
            for url in urls
        ]
        for result in await asyncio.gather(*tasks):
            prefix = "BB0" if "bootbarn.com" in result['url'] else "ET0"
            result['unique_key'] = generate_unique_key(prefix)

            result['created_at'] = current_datetime()
            result['updated_at'] = current_datetime()

            results.append(result)

    return results


async def main_async():
    links_file = "unique_links_bootbarn.json"
    cookies_file = "cookies_bootbarn.json"
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
    output_file = "output_bootbarn.json"
    with open(output_file, 'w') as f:
        json.dump(all_results, f, indent=4)


if __name__ == "__main__":
    asyncio.run(main_async())
