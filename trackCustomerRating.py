import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup


url = 'https://geizhals.de/g-skill-trident-z5-neo-rgb-schwarz-dimm-kit-32gb-f5-6000j3038f16gx2-tz5nr-a2815824.html?hloc=at&hloc=de#links'

def get_reviews(url):
    driver = webdriver.Chrome()
    driver.get(url)

    time.sleep(5) 

    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2) 
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    page_source = driver.page_source
    driver.quit()

    soup = BeautifulSoup(page_source, 'html.parser')
    
    reviews = []
    ratings = []
    
    review_elements = soup.find_all('li', class_='svelte-rjyim6') 
    print(f"Review Elements found: {len(review_elements)}")
    
    for element in review_elements:
        review_text_element = element.find('div', class_='ratings-text') 
        rating_element = element.find('div', class_='rating')  
        
        if review_text_element and rating_element:
            review_text = review_text_element.get_text(strip=True)
            rating = rating_element.get_text(strip=True)
            
            reviews.append(review_text)
            try:
                ratings.append(float(rating.split()[0]))  
            except ValueError:
                continue
    
    return reviews, ratings

# Hauptfunktion
def main():
    reviews, ratings = get_reviews(url)
    
    # Überprüfen die gesammelten Bewertungen und Bewertungen
    with open("output.txt", "w", encoding="utf-8") as f:
        f.write("Gesammelte Bewertungen:\n")
        for review in reviews:
            f.write(review + "\n")
        
        f.write("\nGesammelte Bewertungen:\n")
        for rating in ratings:
            f.write(str(rating) + "\n")

if __name__ == '__main__':
    main()
