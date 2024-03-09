import json
import requests

def fetch_details_from_oxy():
    # Чтение списка URL из файла
    with open('unique_links.json', 'r') as file:
        links = json.load(file)

    results = []  # Список для сохранения результатов

    for url in links:
        # Логика для обработки каждой ссылки, например, вызов API Oxylabs
        response = requests.post(
            'https://realtime.oxylabs.io/v1/queries',
            auth=('wenitwa', 'hellobobbobboB1'),  # Используйте свои реальные данные для аутентификации
            json={
                'source': 'universal_ecommerce',
                'url': url,
                'geo_location': 'United States',
                'parse': True,
            }
        )

        if response.status_code == 200:
            # Обработка успешного ответа и добавление данных в список результатов
            results.append(response.json())
        else:
            # Добавление сообщения об ошибке в список результатов
            results.append({'url': url, 'error': f'Status code {response.status_code}'})

    # Текущая дата и время для создания уникального имени файла

    file_name = f'response_.json'

    # Сохранение результатов в JSON-файл
    with open(file_name, 'w') as json_file:
        json.dump(results, json_file, indent=4)

    print(f"Данные сохранены в файл: {file_name}")

# Тестирование функции
fetch_details_from_oxy()
