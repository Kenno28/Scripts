import requests
import sys
sys.path.append(r'D:\Ana\envs\selenium_env\Lib\site-packages')
from bs4 import BeautifulSoup
import schedule
import time
import csv
from datetime import datetime

# Liste der Produkt-URLs
product_urls = [
    'https://geizhals.de/g-skill-trident-z5-neo-rgb-schwarz-dimm-kit-32gb-f5-6000j3038f16gx2-tz5nr-a2815824.html?hloc=at&hloc=de',
    'https://geizhals.de/adidas-fussball-uefa-euro-2024-trainings-ball-in9366-a3064001.html?hloc=at&hloc=de',
    'https://geizhals.de/adidas-uefa-euro-2024-deutschland-auswaertstrikot-herren-ip8158-a3151533.html?hloc=at&hloc=de',
    'https://geizhals.de/nike-uefa-euro-2024-tuerkei-stadium-heimtrikot-herren-fv1743-100-a3169033.html?hloc=at&hloc=de',
    'https://geizhals.de/nike-uefa-euro-2024-portugal-stadium-heimtrikot-herren-fj4275-657-a3168874.html?hloc=at&hloc=de',
    'https://geizhals.de/adidas-uefa-euro-2024-spanien-heimtrikot-herren-ip9331-a3167205.html?hloc=at&hloc=de',
    'https://geizhals.de/nike-uefa-euro-2024-england-stadium-heimtrikot-herren-fj4285-100-a3168596.html?hloc=at&hloc=de'
]

# Funktion zum Abrufen des Preises und des Namens
def get_product_details(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8' 
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Preis aus dem HTML extrahieren
    price_tag = soup.find('span', class_='gh_price')
    if price_tag:
        price_text = price_tag.get_text(strip=True)
        price = ''.join(filter(lambda x: x.isdigit() or x == ',', price_text))
    else:
        price = None

    # Produktname aus dem HTML extrahieren
    name_tag = soup.find('h1', class_='variant__header__headline')  
    if name_tag:
        name = name_tag.get_text(strip=True)
    else:
        name = None

    return name, price

# Funktion zum Speichern der Details
def save_details(name, price, filename='prices.csv'):
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now().isoformat(), name, price])

# Hauptfunktion, die die Arbeit ausführt
def job():
    for url in product_urls:
        name, price = get_product_details(url)
        if name and price:
            save_details(name, price)
            print(f'Details gespeichert: Name={name}, Preis={price}')
        else:
            print(f'Details konnten nicht abgerufen werden für URL: {url}')

if __name__ == '__main__':
    job()
