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
            driver.set_page_load_timeout(5)

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

            try:
                color_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="product-content"]/div[2]/div/ul/li[2]/div[1]/span/span[2]'))
                )
                color = color_element.text.strip()
                results['color'] = color
            except:
                results['color'] = "Color not found"

            try:
                international_shipment_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="product-content"]/div[1]/span[2]/div/div'))
                )
                international_shipment = international_shipment_element.text.strip()
                if international_shipment == "OOPS, THIS ITEM IS CURRENTLY UNAVAILABLE FOR INTERNATIONAL SHIPMENT":
                    results['international_shipment'] = False
                else:
                    results['international_shipment'] = True
            except:
                results['international_shipment'] = "International shipment not found"


            try:
                item_detail_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="pdpMain"]/div[2]/div[5]/div/div/div/div/ul'))
                )
                item_detail = item_detail_element.text.strip()
                results['item_detail'] = item_detail
            except:
                results['item_detail'] = "Item detail not found"

            # try:
            #     url_on_image_element = WebDriverWait(driver, 5).until(
            #         EC.presence_of_element_located((By.XPATH, '//*[@id="thumbnails"]/div/div/div'))
            #     )
            #     url_on_image = url_on_image_element.get_attribute('href ')
            #     results['url_on_image'] = url_on_image
            # except:
            #     results['url_on_image'] = "Url on image not found"


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
    results = []

    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor(max_workers=15) as executor:
        tasks = [
            loop.run_in_executor(executor, fetch_and_parse, url, cookies, proxies)
            for url in urls
        ]
        for result in await asyncio.gather(*tasks):
            results.append(result)

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