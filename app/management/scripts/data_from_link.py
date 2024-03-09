import requests
from lxml import html
import requests_cache

# Включаем кеширование
requests_cache.install_cache('product_cache', expire_after=300)

def fetch_details(url, xpaths):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Ошибка при запросе страницы: {response.status_code}")
        return None

    tree = html.fromstring(response.content)

    # Словарь для хранения результатов
    results = {}

    # Извлекаем данные для каждого XPath выражения
    for key, xpath in xpaths.items():
        elements = tree.xpath(xpath)
        # Обработка списочных данных
        if isinstance(elements, list) and len(elements) > 0 and hasattr(elements[0], 'text_content'):
            # Для списков элементов извлекаем текст каждого элемента
            results[key] = [element.text_content().strip() for element in elements]
        elif elements:
            # Для одиночных элементов извлекаем текст первого найденного
            results[key] = elements[0].text_content().strip()
        else:
            results[key] = None

    return results


# Список заданий для парсинга: URL и соответствующие XPath выражения
tasks = [
    {
        'url': 'https://www.bootbarn.com/038782.html',
        'xpaths': {
            'product_name': '//*[@id="pdpMain"]/header/div/h1',
            'product_price': '//*[@id="pdpMain"]/div[2]/div[2]/div[1]/div/span[1]/strong',
            'product_description': '//*[@id="pdpMain"]/div[2]/div[4]/div/div/div/div/p[1]',
            'sizes': '//*[@id="product-content"]/div[2]/div/ul/li[1]/div[2]/ul[contains(@class, "size-options")]/li[contains(@class, "selectable")]/a/@data-size-id',
        }
    },
]

for task in tasks:
    print(f"Обрабатывается: {task['url']}")
    details = fetch_details(task['url'], task['xpaths'])
    if details:
        print("Извлеченные данные:")
        for key, value in details.items():
            if isinstance(value, list):
                print(f"{key}:")
                for item in value:
                    print(f" - {item}")
            else:
                print(f"{key}: {value}")
    else:
        print("Невозможно извлечь данные.")
    print("-" * 30)
