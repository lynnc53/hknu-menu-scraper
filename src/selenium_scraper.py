from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

# function to initialize selenium webdriver
# This function sets up the Chrome WebDriver with options for headless operation and GPU acceleration disabled
def get_driver():
    options = Options()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--disable-gpu")  # Disable GPU acceleration
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver 

def extract_current_week(driver):
    soup = BeautifulSoup(driver.page_source, "html.parser")
    rows = soup.select("tr")

    menus = []
    current_date = ""

    for row in rows:
        cells = row.find_all("td")
        if len(cells) == 3:
            current_date = cells[0].get_text(strip=True)
            type_cell = cells[1]
            menu_cell = cells[2]
        elif len(cells) == 2:
            type_cell = cells[0]
            menu_cell = cells[1]        
        else:
            continue

        meal_type = type_cell.get_text(strip=True)
        menu_items = [
            item.strip()
            for item in menu_cell.decode_contents().split("<br>")
            if item.strip()
        ]

        menus.append({
            "Date": current_date,
            "Type": meal_type,
            "Menu": " ".join(menu_items)
        })
    return menus 

# this function clicks the "next week" button to navigate to the next week's menu
def click_previous_week(driver):
    try:
        wait = WebDriverWait(driver, 10)
        button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a._termLeft")))
        button.click()
        time.sleep(1.5)
    except Exception as e:
        print("No previous week button found:", e)
        return False
    return True