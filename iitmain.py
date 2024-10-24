import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import csv

options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)
driver.get("https://josaa.admissions.nic.in/applicant/SeatAllotmentResult/CurrentORCR.aspx")

def Round():
    try:
        div_xpath = '//*[@id="ctl00_ContentPlaceHolder1_ddlroundno_chosen"]'
        chosen_div = driver.find_element(By.XPATH, div_xpath)
        chosen_div.click()
        input_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="chosen-drop"]//input'))
        )
        input_field.send_keys("7")  # Update to the latest round number for 2024 (e.g., Round 7)
        time.sleep(5)
        input_field.send_keys(Keys.ENTER)
        print("Round Completed")
    except Exception as e:
        print(f"Error in Round selection: {e}")

def institute_type():
    try:
        wait = WebDriverWait(driver, 10)
        dropdown = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//div[@id="ctl00_ContentPlaceHolder1_ddlInstype_chosen"]')))
        dropdown.click()
        input_element = driver.find_element(By.XPATH, '//div[@id="ctl00_ContentPlaceHolder1_ddlInstype_chosen"]//input')
        input_element.clear()
        input_element.send_keys("Indian Institute of Technology")
        time.sleep(5)
        input_element.send_keys(Keys.ENTER)
        print("Institute type Completed")
    except Exception as e:
        print(f"Error in Institute type: {e}")

def institute_name():
    try:
        wait = WebDriverWait(driver, 10)
        dropdown = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//div[@id="ctl00_ContentPlaceHolder1_ddlInstitute_chosen"]')))
        dropdown.click()
        input_element = driver.find_element(By.XPATH,
                                            '//div[@id="ctl00_ContentPlaceHolder1_ddlInstitute_chosen"]//input')
        input_element.clear()
        input_element.send_keys("ALL")
        input_element.send_keys(Keys.ENTER)
        time.sleep(5)
        print("Institute Name Completed")
    except Exception as e:
        print(f"Error in Institute name: {e}")

def academic_program():
    try:
        wait = WebDriverWait(driver, 10)
        dropdown = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//div[@id="ctl00_ContentPlaceHolder1_ddlBranch_chosen"]')))
        dropdown.click()
        input_element = driver.find_element(By.XPATH,
                                            '//div[@id="ctl00_ContentPlaceHolder1_ddlBranch_chosen"]//input')
        input_element.clear()
        input_element.send_keys("ALL")
        input_element.send_keys(Keys.ENTER)
        time.sleep(5)
        print("Academic Program Completed")
    except Exception as e:
        print(f"Error in Academic Program: {e}")

def seat_type():
    try:
        wait = WebDriverWait(driver, 10)
        dropdown = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//div[@id="ctl00_ContentPlaceHolder1_ddlSeattype_chosen"]')))
        dropdown.click()
        input_element = driver.find_element(By.XPATH, '//div[@id="ctl00_ContentPlaceHolder1_ddlSeattype_chosen"]//input')
        input_element.clear()
        input_element.send_keys("ALL")
        time.sleep(5)
        input_element.send_keys(Keys.ENTER)
        print("Seat type Completed")
    except Exception as e:
        print(f"Error in Seat type: {e}")

def submit():
    try:
        submit_button = driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_btnSubmit")
        submit_button.click()
        time.sleep(2)
        print("Submit Completed")
    except Exception as e:
        print(f"Error in Submit: {e}")

def exp_data():
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    rows = soup.find_all('tr')
    with open('iitmAIN_2024.csv', 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        headers = ["College", "Branch", "Quota", "Category", "Gender", "OpenRank", "CloseRank"]
        csv_writer.writerow(headers)
        for row in rows:
            columns = row.find_all('td')
            row_data = []
            for column in columns:
                text = column.get_text(strip=True)
                row_data.append(text)
            csv_writer.writerow(row_data)

def national_colleges():
    Round()
    institute_type()
    institute_name()
    academic_program()
    seat_type()
    submit()
    time.sleep(3)
    exp_data()

national_colleges()
