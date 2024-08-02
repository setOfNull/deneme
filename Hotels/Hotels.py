from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
import json
import concurrent.futures
from selenium.webdriver.chrome.options import Options

from multiprocessing import Pool  

adultCount = 2

def bookingScraper(hotel_data):

    options = Options()
    
    driver = webdriver.Chrome(options=options) 
    
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    driver.get(f"https://www.hotels.com/")
        
    try:
        hotelSearchBtn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-stid='destination_form_field-menu-trigger']")))
        hotelSearchBtn.click()
        goingToBtn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "destination_form_field")))
        goingToBtn.send_keys(hotel_data[0])
        
        firstResult = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-stid='destination_form_field-result-item-button']")))
        firstResult.click() 
        
        searchBtn = driver.find_element(By.CSS_SELECTOR,"button[id='search_button']").click() 
        
    except :
        print(f"Hotel not found")
        driver.quit()
        return

    currentURL = driver.current_url

    def update_url_parameters(url, updates):
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        for param, new_value in updates.items():
            if param in query_params:
                query_params[param] = [new_value]
        
        new_query_string = urlencode(query_params, doseq=True)
        new_url = parsed_url._replace(query=new_query_string)
        
        return urlunparse(new_url)
    updates = {
        'd1': hotel_data[1],
        'startDate': hotel_data[1],
        'd2': hotel_data[2],
        'endDate': hotel_data[2],
        'adults': adultCount
    }

    new_url = update_url_parameters(currentURL, updates)
    driver.get(new_url)
    
    try:
        price = driver.find_elements(By.XPATH, '//*[@id="app-layer-base"]/div/main/div/div/div/div/div/div[2]/section[2]/div/div[2]/div/div[2]/div[1]/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div/div/div[1]/div/div')
        driver.implicitly_wait(10)
        print(price[0].get_attribute("innerText"))
        driver.close()
    except:
        print("The hotel is full")



with open("C:/Users/mnuri/Desktop/moledro/Hotels/json/jsonHotel1.json", "r") as my_file:
    hotels = json.load(my_file)
    
hotels = [(h["hotelName"], h["dates"]["checkIn"], h["dates"]["checkOut"]) for h in hotels]

def main():        
    with Pool() as p:
        p.map(bookingScraper,hotels)


if __name__ == '__main__':
    main()

#        for serial type of scraping
# for hotel in hotels:
#     hotel_name = hotel["hotelName"]
#     check_in = (hotel["dates"]["checkIn"])
#     check_out = hotel["dates"]["checkOut"]
#     print()
#     print(f"Hotel Name: {hotel_name}")
#     print(f"Check-In Date: {check_in}")
#     print(f"Check-Out Date: {check_out}") 
#     bookingScraper()



