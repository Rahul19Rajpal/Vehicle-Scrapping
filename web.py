import pandas as pd
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import os
import time

def scrape_images(file_path):
    image_directory = 'public/vehicle_images'
    if not os.path.exists(image_directory):
        os.makedirs(image_directory)

    # Set up Selenium
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    vehicle_data = pd.read_excel(file_path)
    for index, row in vehicle_data.iterrows():
        try:
            brand = row['Brand']
            model = row['Models']
            search_query = f"{brand} {model}".replace(' ', '%20')
            search_url = f'https://ch.pinterest.com/search/pins/?q={search_query}&rs=typed2dname'

            # Open the search URL
            driver.get(search_url)
            time.sleep(3)  # wait for the page to load

            # Find the first image element on the page
            pin_elements = driver.find_elements(By.XPATH, '//a[@href and contains(@href, "/pin/")]')
            if pin_elements:
                first_pin_url = pin_elements[0].get_attribute('href')
                driver.get(first_pin_url)
                time.sleep(3)  # wait for the pin page to load

                image_element = driver.find_element(By.XPATH, '//img[contains(@src, "pinimg")]')
                image_url = image_element.get_attribute('src')
                print(image_url)
                # Download the image
                image_filename = f'{image_directory}/{brand}_{model}.jpg'.replace(' ', '_')
                with open(image_filename, 'wb') as f:
                    image_response = requests.get(image_url)
                    f.write(image_response.content)
                print(f"Downloaded image for {brand} {model}")
            else:
                print(f"No pins found for {brand} {model}")

        except Exception as e:
            print(f"Error while processing {brand} {model}: {e}")

    driver.quit()

# Set the file path directly in the script
file_path = r'D:\vechicle scrapping\vehicle_image_scraper\Vehicle Model.xlsx'
scrape_images(file_path)
