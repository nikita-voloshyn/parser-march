import os
import json
import hashlib
import requests
import requests_cache
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Enable caching
requests_cache.install_cache('web_cache', expire_after=3600)  # Cache expires after 1 hour

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36")

def fetch_and_parse(url):
    results = {'url': url}

    # Check if response is cached
    response = requests.get(url)
    try:
        # Read data from cache if available
        cached_data = response.json()
        results.update(cached_data)
    except json.JSONDecodeError:
        # Fetch data and parse
        with webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options) as driver:
            driver.get(url)

            print(driver.page_source)

            try:
                product_name_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="listing-page-cart"]/div[4]/h1'))
                )
                name = product_name_element.text.strip()
                results['name'] = name
            except:
                results['name'] = "Name not found"

            # try:
            #     size_options = WebDriverWait(driver, 10).until(
            #         EC.presence_of_all_elements_located((By.XPATH, '//*[@id="variation-selector-0"]'))
            #     )
            #     sizes = [option.text.strip() for option in size_options if option.get_attribute('value') != '0']
            #     results['sizes'] = sizes
            # except:
            #     results['sizes'] = "Sizes not found"

        # Cache the response
        requests.get(url)

    return results


def read_links_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        return data

def main():
    links_file = "unique_links.json"
    output_file = "output.json"

    links = read_links_from_file(links_file)
    output_data = []

    for url in links:
        print(f"Processing: {url}")
        result = fetch_and_parse(url)
        output_data.append(result)

    with open(output_file, 'w') as f:
        json.dump(output_data, f, indent=4)

if __name__ == "__main__":
    main()
