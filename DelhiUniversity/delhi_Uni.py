import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import csv

def init_driver(chrome_driver_path=None):
    options = webdriver.ChromeOptions()
    if chrome_driver_path:
        return webdriver.Chrome(executable_path=chrome_driver_path, options=options)
    return webdriver.Chrome(options=options)

def write_to_csv(filename, data):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["College-name", "Program", "Category", "Gender", "Cutoff"])  # Desired column arrangement
        for row_data in data:
            csv_writer.writerow(row_data)

def fetch_cutoff_data(heading_text, filename):
    driver = init_driver()
    try:
        driver.get("https://www.shiksha.com/science/articles/cuet-du-cut-off-blogId-129629")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "h2"))
        )
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        # Locating the heading for the specific cutoff round
        cutoff_heading = soup.find('h2', string=heading_text)
        if not cutoff_heading:
            print(f"Error: '{heading_text}' heading not found.")
            return
        table = cutoff_heading.find_next('table')
        if not table:
            print("Error: No table found after the heading.")
            return

        cutoff_data = []
        rows = table.find_all('tr')
        count = 0
        for row in rows:
            columns = row.find_all(['th', 'td'])
            row_data = [col.get_text(strip=True) for col in columns]
            # Rearranging the columns based on desired order:
            if len(row_data) == 4 and count>0:
                if(college_name.find("W")==-1):
                    gender = "Gender-Neutral"
                else:
                    gender = "Female-only"
                arranged_data = [
                    college_name, # College name 
                    row_data[0],  # Program
                    row_data[1],  # Category
                    gender,  # Gender
                    row_data[2],  # Cutoff-Rank
                ]
                cutoff_data.append(arranged_data)
            elif len(row_data) == 1:
                college_name = row_data[0]
                count = 1

        write_to_csv(filename, cutoff_data)
        print(f"Data scraped and saved to {filename} successfully.")

    except Exception as e:
        print(f"An error occurred during scraping for {heading_text}: {e}")
    
    finally:
        driver.quit()

def main():
    fetch_cutoff_data("CUET DU 2024 First Cut Off", 'du_cutoff_2024_first.csv')
    fetch_cutoff_data("CUET DU 2024 Second Cut Off", 'du_cutoff_2024_second.csv')

if __name__ == "__main__":
    main()
