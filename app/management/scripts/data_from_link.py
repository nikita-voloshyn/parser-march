import requests
from lxml import html
import requests_cache
import json
import re

# Включаем кеширование
requests_cache.install_cache('product_cache', expire_after=300)


def load_links_from_file(file_name):
    with open(file_name, 'r') as file:
        links = json.load(file)
    return links


def extract_product_id_from_url(url):
    match = re.search(r'/(\d+).html', url)
    return match.group(1) if match else None


def fetch_details(url, xpaths):
    response = requests.get(url)
    if response.status_code != 200:
        return None
    tree = html.fromstring(response.content)
    results = {}
    for key, xpath in xpaths.items():
        elements = tree.xpath(xpath)
        results[key] = elements[0].text_content().strip() if elements else None
    return results


def fetch_product_details_from_api(pid):
    url = "https://www.bootbarn.com/on/demandware.store/Sites-bootbarn_us-Site/default/Product-GetVariationAttributes"
    data = {"pid": pid}
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, data, headers)
    return response.json() if response.status_code == 200 else None


def process_product_data(product_data, details, pid):
    available_sizes = [value for variation in product_data['variations']
                       if variation['productVariationAttribute'] == 'size'
                       for value in variation['values'] if value['stock'] == 'In Stock']

    if not available_sizes:  # Если нет доступных размеров, возвращаем None
        return None

    return {
        'product_id': pid,
        'product_name': details['product_name'],
        'product_price': details['product_price'],
        'product_description': details['product_description'],
        'available_sizes': available_sizes
    }


links = load_links_from_file('unique_links.json')

xpaths = {
    'product_name': '//*[@id="pdpMain"]/header/div/h1',
    'product_price': '//*[@id="pdpMain"]/div[2]/div[2]/div[1]/div/span[1]/strong',
    'product_description': '//*[@id="pdpMain"]/div[2]/div[4]/div/div/div/div/p[1]',
}

all_products_info = []

for url in links:
    pid = extract_product_id_from_url(url)
    if pid:
        details = fetch_details(url, xpaths)
        if details:
            product_data = fetch_product_details_from_api(pid)
            if product_data:
                product_info = process_product_data(product_data, details, pid)
                if product_info:  # Добавляем продукт только если он имеет доступные размеры
                    all_products_info.append(product_info)
            else:
                print(f"Невозможно извлечь данные о размерах через API для продукта {pid}.")
        else:
            print(f"Невозможно извлечь данные с веб-страницы для продукта {pid}.")

# Сохранение всей собранной информации о продуктах в один файл
with open('all_products_details.json', 'w') as json_file:
    json.dump(all_products_info, json_file, indent=4)

print("Вся информация о продуктах успешно сохранена в 'all_products_details.json'")
