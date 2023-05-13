from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import time
import csv
import os
import dotenv

# Загрузка настроек из файла .env
from dotenv import load_dotenv
load_dotenv()

last_page = 2

base_url = "https://app.dealroom.co/"
firms_data = []

# Получение учетных данных прокси-сервера из переменных окружения
PROXY_USERNAME = os.getenv('PROXY_USERNAME')
PROXY_PASSWORD = os.getenv('PROXY_PASSWORD')

# Указание настроек прокси-сервера
PROXY_HOST = "zproxy.lum-superproxy.io"
PROXY_PORT = "22225"

# Создание сессии
session = requests.Session()
session.proxies = {
    'http': f"http://{PROXY_USERNAME}:{PROXY_PASSWORD}@{PROXY_HOST}:{PROXY_PORT}",
    'https': f"http://{PROXY_USERNAME}:{PROXY_PASSWORD}@{PROXY_HOST}:{PROXY_PORT}"
}

# отключение предупреждений InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# отключение проверки SSL-сертификатов
response = requests.get('https://example.com', verify=False)

# Создаем список для хранения всех ссылок на врачей
all_dealroom_links = []

page = 1
# Создаем глобальный счетчик
counter = 1

# Создаем цикл для перебора всех страниц
while True:
    # Формируем ссылку на текущую страницу
    url = f'https://app.dealroom.co/lists/33805?sort=-startup_ranking_rating'

    # Загружаем страницу
    response = session.get(url)

    # Ожидание загрузки страницы
    time.sleep(5)

    # Получение HTML-кода страницы с результатами поиска
    soup = BeautifulSoup(response.content, 'html.parser')

    links = soup.select('div.table-list-item div.table-list-columns-fixed div.table-list-column name div.entity-name div.entity-name__info div.type-element a[href]')
    all_dealroom_links = [urljoin(base_url, link['href']) for link in links]

    # Создаем цикл для перебора всех врачей
    for dealroom_link in all_dealroom_links:
        print(dealroom_link)

        # Загружаем страницу фирмы
        response = session.get(dealroom_link)

        # Ожидание загрузки страницы
        time.sleep(5)

        # Получение HTML-кода страницы фирмы
        soup = BeautifulSoup(response.content, 'html.parser')

        # Извлечение данных фирмы
        try:
            name = soup.select_one('h1.name').get_text(strip=True)
        except AttributeError:
            name = 'No name data'
        try:
            description = soup.select_one('div.item-details-info__details div.tagline').get_text(strip=True)
        except AttributeError:
            description = 'No description data'
        try:
            website = soup.select_one('div.entity-details div.details div.item-details-info__website a[href]').get_text(strip=True)
        except AttributeError:
            website = 'No website data'
        try:
            span_element = soup.select_one('div.resource-urls')
            if span_element:
                index = span_element.text.find("linkedin")
                if index != -1:
                    linkedin = span_element.select_one('a[href*=linkedin]').get('href')
                else:
                    linkedin = 'No LinkedIn data'
            else:
                linkedin = 'No LinkedIn data'
        except AttributeError:
            linkedin = 'No LinkedIn data'
            # Добавляем данные в список
    firm_data = {'Name': name, 'Description': description, 'Website': website, 'LinkedIn': linkedin}
    firms_data.append(firm_data)

    # Выводим информацию о прогрессе выполнения
    print(f'Processed {counter} firm(s).')

    # Увеличиваем значение счетчика на единицу
    counter += 1

    # Условие выхода из цикла
    if page >= last_page:
        break
    else:
        page += 1

# Сохраняем результаты в CSV-файл
with open('dealroom_data.csv', 'w', newline='', encoding='utf-8') as file:
    fieldnames = ['Name', 'Description', 'Website', 'LinkedIn']
writer = csv.DictWriter(file, fieldnames=fieldnames)
writer.writeheader()
for firm_data in firms_data:
    writer.writerow(firm_data)