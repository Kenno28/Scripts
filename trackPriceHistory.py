import time
import pandas as pd
import matplotlib.pyplot as plt
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import re
import json

# URL der Seite
url = 'https://gotecher.com/apple-airpods-max-wireless-over-ear-headphones-active-noise-cancelling-transparency-mode'

service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
driver.get(url)

# Warten, bis die Seite vollständig geladen ist
time.sleep(5)

# Extrahieren der Preisdaten 
script_tags = driver.find_elements(By.TAG_NAME, 'script')

for index, script in enumerate(script_tags):
    script_content = script.get_attribute('innerHTML')

labels = None
data = None
for script in script_tags:
    script_content = script.get_attribute('innerHTML')
    if 'new Chart(ctx' in script_content:
        print("Found script with Chart.js data.")
        labels_match = re.search(r'labels: (\[.*?\])', script_content)
        data_match = re.search(r'data: (\[.*?\])', script_content)
        if labels_match and data_match:
            labels = labels_match.group(1)
            data = data_match.group(1)
        break

# Schließen des WebDrivers
driver.quit()

# Umwandeln der extrahierten Daten in ein DataFrame
if labels and data:
    labels_list = json.loads(labels)
    data_list = json.loads(data)
    df = pd.DataFrame({'date': labels_list, 'price': data_list})
    df['date'] = pd.to_datetime(df['date'])
    df['price'] = pd.to_numeric(df['price'])
    df.sort_values('date', inplace=True)


    # Visualisieren der Preisdaten
    plt.figure(figsize=(10, 5))
    plt.plot(df['date'], df['price'], marker='o')
    plt.title('Product Price History')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.grid(True)

    # Setzen der Grenzen für die Y-Achse
    plt.ylim(min(df['price']) - 10, max(df['price']) + 10)

    plt.show()
else:
    print("Keine Preisdaten gefunden.")
