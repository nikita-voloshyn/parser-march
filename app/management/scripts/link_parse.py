from bs4 import BeautifulSoup
import re

# HTML содержимое, полученное в ответе
html_content = ""

soup = BeautifulSoup(html_content, 'html.parser')

# Паттерн для поиска необходимых ссылок
pattern = re.compile(r'/listings/.+?/(\d+)')

# Множество для хранения уникальных ссылок
unique_links = set()

# Поиск всех ссылок с атрибутом 'href', которые соответствуют нашему паттерну
for a in soup.find_all('a', href=True):
    match = pattern.search(a['href'])
    if match:
        unique_id = match.group(1)
        link = f"https://www.bonanza.com/listings/{unique_id}"
        unique_links.add(link)

# Вывод уникальных ссылок
for link in unique_links:
    print(link)
