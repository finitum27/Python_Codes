from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.firefox import GeckoDriverManager
import pandas as pd
import json
from bs4 import BeautifulSoup
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Selenium WebDriver setup with headless mode
options = Options()
options.headless = False  # Set to True if you don't need to see the browser

driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)

def login_to_linkedin(email, password):
    try:
        driver.get('https://www.linkedin.com/login')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'username')))
        driver.find_element(By.ID, 'username').send_keys(email)
        driver.find_element(By.ID, 'password').send_keys(password)
        driver.find_element(By.XPATH, '//button[@type="submit"]').click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//nav')))
        logging.info("Logged in successfully")
    except TimeoutException:
        logging.error("Login page did not load correctly or took too long.")
    except NoSuchElementException as e:
        logging.error(f"Login element not found: {e}")

def fetch_page_content(url):
    try:
        driver.get(url)
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        return driver.page_source
    except TimeoutException:
        logging.error(f"Timeout while fetching page source for {url}")
        return None
    except Exception as e:
        logging.error(f"Error fetching page source for {url}: {e}")
        return None

def parse_company_data(page_source):
    if not page_source:
        return []

    soup = BeautifulSoup(page_source, 'html.parser')
    company_name = soup.find('title').text.strip() if soup.find('title') else 'N/A'
    
    employees = []
    employee_cards = soup.find_all('div', {'class': 'org-people-profile-card__profile-title'})  # Update this selector

    for card in employee_cards:
        name = card.get_text(strip=True)
        designation = card.find_next_sibling('div', {'class': 'org-people-profile-card__profile-title'})  # Adjust this selector
        location = card.find_next_sibling('div', {'class': 'org-people-profile-card__location'})  # Adjust this selector

        employees.append({
            'Company Name': company_name,
            'Employee Name': name,
            'Designation': designation.get_text(strip=True) if designation else 'N/A',
            'Location': location.get_text(strip=True) if location else 'N/A'
        })

    return employees

def save_to_csv(data, file_name):
    df = pd.DataFrame(data)
    df.to_csv(file_name, index=False, encoding='utf-8')
    logging.info(f"Data saved to {file_name}")

def save_to_excel(data, file_name):
    df = pd.DataFrame(data)
    df.to_excel(file_name, index=False)
    logging.info(f"Data saved to {file_name}")

def main():
    email = 'caefreelancing27@gmail.com'
    password = 'webscrap27'
    
    login_to_linkedin(email, password)
    
    url = 'https://www.linkedin.com/company/stangroupco/'
    page_source = fetch_page_content(url)
    
    if page_source:
        company_data = parse_company_data(page_source)
        file_name_csv = 'company_data.csv'
        file_name_excel = 'company_data.xlsx'
        
        save_to_csv(company_data, file_name_csv)
        save_to_excel(company_data, file_name_excel)
    else:
        logging.error(f"No data found in {url}")
    
    driver.quit()

if __name__ == "__main__":
    main()
