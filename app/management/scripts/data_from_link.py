import os
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

chrome_options = Options()
chrome_options.add_argument("--headless")  # Hides the browser window
chrome_options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36")


def load_proxies(file_path):
    with open(file_path, 'r') as f:
        proxies = f.read().splitlines()
    return proxies


def save_proxies(file_path, proxies):
    with open(file_path, 'w') as f:
        f.write('\n'.join(proxies))


def load_cookies_from_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        cookies = json.load(file)
    return cookies


def fetch_and_parse(url, cookies, proxies):
    results = {'url': url, 'sizes': [], 'colors': []}

    while proxies:
        proxy = proxies.pop(0)
        print(f"Using proxy: {proxy}")

        # Fetch data and parse
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        driver.get(url)
        driver.set_page_load_timeout(5)  # Set a timeout for page loading

        try:
            product_name_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="listing-page-cart"]/div[4]/h1'))
            )
            name = product_name_element.text.strip()
            results['name'] = name
        except:
            results['name'] = "Name not found"

        try:
            item_detail_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="wt-content-toggle-product-details-read-more"]/p'))
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

        driver.quit()  # Close the WebDriver session

        # If request succeeds, break out of the loop
        break

    return results


def read_links_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        return data


def main():
    # File paths
    links_file = "unique_links.json"
    output_file = "output.json"
    cookies_file = "cookies.json"
    proxies_file = "proxies.txt"

    if not os.path.exists(cookies_file):
        print("File with cookies not found.")
        return

    cookies = load_cookies_from_json(cookies_file)
    links = read_links_from_file(links_file)
    proxies = load_proxies(proxies_file)
    output_data = []  # Define output_data here

    for url in links:
        print(f"Processing: {url}")
        result = fetch_and_parse(url, cookies, proxies)
        output_data.append(result)

    # Write output data to a JSON file
    with open(output_file, 'w') as f:
        json.dump(output_data, f, indent=4)


if __name__ == "__main__":
    main()

