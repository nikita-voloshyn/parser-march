import os
import json
import random

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
    results = {'url': url, 'sizes': [], 'colors': []}

    random_user_agent = get_random_user_agent()

    # Используем случайный заголовок
    chrome_options = Options()
    chrome_options.add_argument(f"user-agent={random_user_agent}")
    while proxies:
        proxy = proxies.pop(0)
        print(f"Using proxy: {proxy}")

        # Fetch data and parse
        with webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options) as driver:
            driver.get(url)
            driver.set_page_load_timeout(5)  # Set a timeout for page loading

            try:
                product_name_element = WebDriverWait(driver, 10).until(
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
                item_detail_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="wt-content-toggle-product-details-read-more"]/p'))
                )
                item_detail = item_detail_element.text.strip()
                results['item_detail'] = item_detail
            except:
                results['item_detail'] = "Item detail not found"

            try:
                color_options = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="variation-selector-1"]'))
                )
                sizes_text = color_options.text.strip()
                sizes = sizes_text.split('\n')
                for size in sizes:
                    if size != "Select a size":
                        results['sizes'].append({'size': size})
            except:
                results['sizes'] = "Sizes not found"

            try:
                color_options = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="variation-selector-0"]'))
                )
                color_text = color_options.text.strip()
                colors = color_text.split('\n')
                for color in colors:
                    if color != "Select a color":
                        results['colors'].append({'color': color})
            except:
                results['colors'] = "Colors not found"

            # If request succeeds, break out of the loop
            break

    return results


def read_links_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        return data

def main():
    links_file = "unique_links.json"
    output_file = "output.json"
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
    output_data = []

    for url in links:
        print(f"Processing: {url}")
        result = fetch_and_parse(url, cookies, proxies)
        output_data.append(result)

    with open(output_file, 'w') as f:
        json.dump(output_data, f, indent=4)

if __name__ == "__main__":
    main()
