import datetime
import os
import json
import random
import re
import asyncio
import uuid
from concurrent.futures import ThreadPoolExecutor
import datetime
from dataclasses import dataclass
import re
from typing import Optional, Dict, List, Union
from fractions import Fraction

import logging

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager

logger = logging.getLogger(__name__)


@dataclass
class ProductVariant:
    price: float
    title: str
    description: str
    color: str
    international_shipment: bool
    unique_key: str
    created_at: str
    updated_at: str
    size: float
    width: str
    gender: str
    image_links: List[str]


@dataclass
class ProductData:
    url: str
    variants: List[ProductVariant]


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


def generate_unique_key(url, color):
    return f"{url.split('/')[-1]}_{color}_{uuid.uuid4().hex[:9]}"


def current_datetime():
    return datetime.datetime.now().isoformat()


def parse_size(size_string: str) -> Optional[Dict[str, Union[float, str]]]:
    match = re.match(r'(\d+(?:\.\d+)?)\s*(?:([^0-9\s]+)\s*)?(?:([\d\s]+(?:\/\d+)?)\s*)?(\D*)', size_string)
    if match:
        size = float(match.group(1))
        if size == int(size):
            size = int(size)
        width = ''
        if match.group(2):
            if '/' in match.group(2):
                fraction = Fraction(match.group(2))
                size += fraction.numerator / fraction.denominator
                width = ''
            else:
                try:
                    width = float(match.group(2))
                except ValueError:
                    width = match.group(2)
        elif match.group(3):
            width = match.group(3)
            if match.group(4):
                width += match.group(4)
        return {'size': size, 'width': width if width else ''}
    elif size_string.strip().isalpha():
        return {'size': size_string.strip(), 'width': ''}
    else:
        return {'size': None, 'width': ''}


def fetch_and_parse(url, cookies, proxies):
    results = {'url': url, 'sizes': [], 'price': 0, 'name': '', 'item_detail': '', 'color': '', 'image_links': []}

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
                name = product_name_element.text[13:].replace('\n', ' ').strip()
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
                                (By.XPATH,
                                 '//*[@id="product-content"]/div[2]/div/ul/li[2]/div[2]/ul/li/a[@data-size-id]')
                            )
                        )
                        sizes = [parse_size(size_element.get_attribute("data-size-id")) for size_element in
                                 size_elements if size_element.get_attribute("same-day-shipping") == "true"]
                        results['sizes'] = sizes
                    except TimeoutException:
                        results['sizes'] = "Sizes not found"

                    try:
                        item_detail_element = WebDriverWait(driver, 5).until(
                            EC.presence_of_element_located(
                                (By.XPATH, '//*[@id="pdpMain"]/div[2]/div[5]/div/div/div/div/ul'))
                        )
                        item_detail = item_detail_element.text.replace('\n', ' ').strip()
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

                    try:
                        # Находим все элементы с классом "thumbnail-link"
                        elements = driver.find_elements(By.CLASS_NAME, 'thumbnail-link')
                        image_links = []
                        for element in elements:
                            try:
                                # Получаем значение атрибута "href" из элемента
                                href = element.get_attribute('href')
                                image_links.append(href)
                            except Exception as e:
                                print(f"Failed to extract link from element: {e}")
                                # Если произошла ошибка при извлечении ссылки, продолжаем выполнение цикла

                        # Добавляем список ссылок на изображения в результаты
                        results['image_links'] = image_links

                        print("Image links extracted successfully.")

                    except Exception as e:
                        print("An error occurred while extracting image links:", e)


            except:
                results['international_shipment'] = "International shipment not found"

            try:
                # Получаем название продукта из результатов
                name = results.get('name', '')

                # Проверяем, содержит ли название продукта целые слова "men" или "women"
                if re.search(r'\bmen\b', name, re.IGNORECASE):
                    gender = 'M'
                elif re.search(r'\bwomen\b', name, re.IGNORECASE):
                    gender = 'F'
                else:
                    gender = 'U'  # По умолчанию

                # Добавляем информацию о поле в результаты
                results['gender'] = gender

            except Exception as ex:
                print(f"Error occurred while determining gender: {ex}")

            print(f"Successfully fetched data for URL: {url}")  # Added print
            break

    return results


def read_links_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        return data


async def fetch_multiple(urls, cookies, proxies, all_results):
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor(max_workers=50) as executor:
        tasks = [
            loop.run_in_executor(executor, fetch_and_parse, url, cookies, proxies)
            for url in urls
        ]
        for result in await asyncio.gather(*tasks):
            product_variants = []

            if 'sizes' not in result:
                continue  # Skip this result if 'sizes' is missing

            if not result.get('international_shipment', False):
                # Создаем запись только с URL-адресом
                product_data = ProductData(url=result['url'], variants=[])
                all_results.append(product_data)
            else:
                # Создаем варианты продукта для каждого размера и цвета
                for size in result['sizes']:
                    unique_key = generate_unique_key(result['url'], result['color'])
                    variant = ProductVariant(
                        price=result.get('price', 0),
                        title=result.get('name', ''),
                        description=result.get('item_detail', ''),
                        color=result.get('color', ''),
                        international_shipment=True,
                        unique_key=unique_key,
                        created_at=current_datetime(),
                        updated_at=current_datetime(),
                        size=size['size'],
                        width=size.get('width', ''),
                        gender=result.get('gender', 'U'),
                        image_links=result.get('image_links', [])
                    )
                    product_variants.append(variant)

                # Создаем запись с вариантами продукта
                product_data = ProductData(url=result['url'], variants=product_variants)
                all_results.append(product_data)

    return all_results


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
    all_results = []
    all_results = await fetch_multiple(links, cookies, proxies, all_results)

    # Записываем все результаты в файл как один JSON-объект
    all_product_data = [{'url': result.url, 'variants': [vars(variant) for variant in result.variants]} for result in
                        all_results]
    output_file = "output_bootbarn.json"
    with open(output_file, 'w') as f:
        json.dump(all_product_data, f, indent=4)


if __name__ == "__main__":
    asyncio.run(main_async())
