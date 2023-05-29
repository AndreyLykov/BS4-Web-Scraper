import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
import time

class Scraper:
    def __init__(self, site):
        self.site = site
    
    def scrape(self):
        # Use requests to get the initial page source
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(self.site, headers=headers)
        html = response.content

        # Set up Selenium with a webdriver
        driver = webdriver.Chrome()
        driver.get(self.site)

        time.sleep(60)

        # Extract the page source after JavaScript execution
        html = driver.page_source

        # Parse the HTML with BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')

        speakers = []  # Empty list to store speaker data

        for tag in soup.find_all("div", class_="speaker__content__inner"):
            speaker_text = " ".join(tag.get_text(strip=True).split())
            speakers.append(speaker_text)
        
        # Create a pandas DataFrame with the speaker data
        df = pd.DataFrame(speakers, columns=["Speaker"])
        
        # The path to the file
        file_path = r"C:\Users\shogu\OneDrive\Документы\Python\WebScraper\Scraper_code\attendees.xlsx"
        
        # Generate the Excel file with the DataFrame
        df.to_excel(file_path, sheet_name="Attendees", index=False)
        
        print(f"Data saved to {file_path}")


page = "https://collisionconf.com/speakers"
Scraper(page).scrape()
