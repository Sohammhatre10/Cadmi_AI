'''We will use "Shiksha.com" to easily scrape the cutoff data 
without logging in the CUET portal which requires Application number, phone no. 
and other sensitive information'''

# Scrapes the first round cutoff of CUET for Delhi University

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import csv

options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)

def fetch_du_First_cutoff():
    """
    Scrapes the DU 2024 cutoff data starting from the heading 'CUET DU 2024 First Cut Off',
    including college names that are specified in <th colspan="4"> elements.

    This function uses Selenium to load the page, then BeautifulSoup to navigate to the heading 
    and extract the cutoff data from the subsequent tables or content, saving it to a CSV file.

    Additionally, adds one blank line after each college's cutoff data in the CSV file.
    
    Returns:
        None
    """
    try:
        driver.get("https://www.shiksha.com/science/articles/cuet-du-cut-off-blogId-129629")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "h2"))
        )
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        
        # Locating the heading 'CUET DU 2024 First Cut Off'
        cutoff_heading = soup.find('h2', text="CUET DU 2024 First Cut Off")
        if not cutoff_heading:
            print("Heading not found.")
            return
        table = cutoff_heading.find_next('table')
        if not table:
            print("No table found after the heading.")
            return
 
        with open('du_cutoff_2024_First.csv', 'w', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)
            rows = table.find_all('tr')
            for row in rows:
                th_college_name = row.find('th', colspan="4")
                if th_college_name:
                    csv_writer.writerow([])  # Adds a blank line after college details
                columns = row.find_all(['th', 'td'])
                row_data = [column.get_text(strip=True) for column in columns]
                if row_data:
                    csv_writer.writerow(row_data)

                

        print("Cutoff data scraped and saved successfully.")
    
    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        driver.quit()

fetch_du_First_cutoff()
