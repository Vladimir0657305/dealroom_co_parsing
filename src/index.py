from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.proxy import Proxy, ProxyType
from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Chrome
from bs4 import BeautifulSoup
from bs4.element import Tag
import re
import os
import dotenv
import requests
import time
from selenium.common.exceptions import TimeoutException
from urllib.parse import urljoin
import csv

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

proxy = Proxy({
    'proxyType': 'MANUAL',
    'httpProxy': f"{PROXY_USERNAME}:{PROXY_PASSWORD}@{PROXY_HOST}:{PROXY_PORT}"
})

# Опции браузера Chrome
chrome_options = Options()
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument("--proxy-server=http://%s" % proxy.no_proxy)

# Указание пути к исполняемому файлу драйвера Chrome
driver_path = "C:/Program Files/Pyton/chromedriver"

# Инициализация драйвера Chrome
driver = webdriver.Chrome(service=Service(executable_path=driver_path), options=chrome_options)

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
    driver.get(url)

    # Прокручиваем страницу до конца
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Ожидание загрузки страницы
    wait = WebDriverWait(driver, 5)
    # wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.diversity')))

    # Получение HTML-кода страницы с результатами поиска
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    # links = soup.select('.docresults a[href]')
    links = soup.select('div.table-list-item div.table-list-columns-fixed div.table-list-column name div.entity-name div.entity-name__info div.type-element a[href]')
    all_dealroom_links = [urljoin(base_url, link['href']) for link in links]

    # Создаем цикл для перебора всех врачей
    for dealroom_link in all_dealroom_links:
        print(dealroom_link)
        # Загружаем страницу фирмы
        driver.get(dealroom_link)
        # Ожидание загрузки страницы
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.card__content')))
        print('GET')

    # Получение HTML-кода страницы фирмы
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        print('WORKING')
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
                    linkedin_element = span_element.find_parent('a')['href']
        except AttributeError:
            linkedin_element = 'No linkedin data'
        try:
            # launch_date = soup.select_one('div.title-tagline div.item-details-info__details div.entity-details div.details div.field-list div.field div.description date-time-range').get_text(strip=True)
            time_element = soup.find('time')
            launch_date = time_element.text.strip()
        except AttributeError:
            launch_date = 'No launch_date data'
        try:
            employees = soup.find('div.description span a').text.strip()
        except AttributeError:
            employees = 'No employees data'

        try:
            ubication = soup.find('div', {'class': 'company-locations'}).span.text.strip()
        except AttributeError:
            ubication = 'No HQ Ubication data'
        
    
    # Добавляем данные врача в список
        # firms_data.append([counter, name, qualifications, specialty, address, telephone, email, website])
        firms_data.append({
            'Counter': counter,
            'Name': name,
            'Description': description,
            'Website': website
            'Linkedin': linkedin_element,
            'Launch_date': launch_date,
            'Employees': employees,
            'Ubication': ubication,
            
        })

# Печатаем данные для проверки
        for firm in firms_data:
            print(firm)

    # Увеличиваем глобальный счетчик на 1
        counter += 1

    # Проверяем, является ли текущая страница последней
    if page == last_page:
        break
    # Увеличиваем значение счетчика цикла
    page += 1
# Закрываем браузер
driver.quit()

# Записываем данные в файл CSV
import csv

with open('firms_data.csv', mode='w', encoding='utf-8', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Counter','Name', 'Description', 'Website', 'Linkedin', 'Launch_date', 'Employees', 'Ubication'])
    for firm in firms_data:
        # print(doctor)
        writer.writerow(firm.values())

print('Data has been scraped and saved to firms_data.csv')


