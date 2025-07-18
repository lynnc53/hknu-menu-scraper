from selenium import webdriver
from selenium.webdriver.common.by import By # for locating HTML elements
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.chrome.options import Options # allows cutomization of the Chrome browser
from webdriver_manager.chrome import ChromeDriverManager # automaticall downloads correct version of ChromeDriver 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC # expected conditions for waiting for elements to load
from bs4 import BeautifulSoup
import time
import re 
import pandas as pd
from datetime import datetime, timedelta
from src.extract_main_menu import extract_main_menu

def get_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")  
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver 

def extract_current_week(driver):
    soup = BeautifulSoup(driver.page_source, "html.parser")
    rows = soup.select("tr")
    yummy_menus = []
    healthy_menus = []
    current_date = ""
    seen_entries = set()  # to track seen entries and avoid duplicates

    for row in rows:
        date_cell = row.find("th")
        if date_cell:
            text = date_cell.get_text(strip=True)
            match = re.search(r'\(\s*([월화수목금토일])\s*\)', text)
            if match:
                weekday = match.group(1)
                if weekday in ["토", "일"]:
                    continue  # skip Sat & Sun
                current_date = text

        cells = row.find_all("td")
        if len(cells) != 2:
            continue 

        meal_type = cells[0].get_text(strip=True)
        menu_items = cells[1].get_text(strip=False).replace("\n", ", ").strip()
        # extract the first item as the main menu eiter separated by a comma or a bracket
        # if the first item is 백미밥, then take the next item
        main_menu = extract_main_menu(menu_items)
        # remove duplicates 
        entry_key = (current_date, meal_type)
        if entry_key in seen_entries:
            continue # skip duplicates 
        seen_entries.add(entry_key)

        entry = {
            "Date": current_date,
            "Meal Type": meal_type,
            "Menu Items": menu_items,
            "Main Menu": main_menu
        }
        if meal_type == "맛난한끼(11:30~13:30)":
            yummy_menus.append(entry)
        elif meal_type == "건강한끼(11:30~13:30)":
            healthy_menus.append(entry)
    return yummy_menus, healthy_menus

def extract_exam_schedule(driver):
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    date_tags = soup.select("p.list-date")
    content_tags = soup.select("p.list-content")

    exam_schedule = []

    for date_tag, content_tag in zip(date_tags, content_tags):
        raw_date = date_tag.get_text(strip=True)
        content_text = content_tag.get_text(strip=True)

        # Check if it's a date range: MM.DD ~ MM.DD
        match_range = re.search(r'(\d{2})[.-](\d{2}).*~.*(\d{2})[.-](\d{2})', raw_date)
        if match_range:
            start_month, start_day, end_month, end_day = match_range.groups()
            start_date = datetime.strptime(f"2025-{start_month}-{start_day}", "%Y-%m-%d")
            end_date = datetime.strptime(f"2025-{end_month}-{end_day}", "%Y-%m-%d")

            current_date = start_date
            while current_date <= end_date:
                exam_schedule.append({
                    "Date": current_date.date(),
                    "Content": content_text
                })
                current_date += timedelta(days=1)
        else:
            # Single date case
            match = re.search(r'(\d{2})[.-](\d{2})', raw_date)
            if not match:
                print(f"Skipping unrecognized date format: {raw_date}")
                continue

            month, day = match.groups()
            date_str = f"2025-{month}-{day}"
            try:
                date_obj = pd.to_datetime(date_str)
                if 3 <= date_obj.month <= 6:
                    exam_schedule.append({
                        "Date": date_obj.date(),
                        "Content": content_text
                    })
            except Exception as e:
                print(f"Failed to parse date '{date_str}': {e}")
                continue

    return exam_schedule


def click_previous_week(driver):
    try:
        wait = WebDriverWait(driver,10)
        button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a._termLeft")))
        button.click()
        time.sleep(1.5)
    except Exception as e:
        print(f"Error clicking previous week button: {e}")
        return False
    return True             