# main scraping logic 
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from src.utils import build_url 

def scrape_week(date_str):
    """
    Scrape one week's menu from HKNU given a Monday date string 'YYYY.MM.DD'.
    returns two lists of dictS: yummy and healthy menus.
    """
    url = build_url(date_str)
    res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, verify=False) # make a GET request
    soup = BeautifulSoup(res.content, "html.parser") # parse the HTML content
    rows = soup.select("table tbody tr") # select all rows in the table

    yummy, healthy = [], [] # initialize lists for yummy and healthy menus
    current_date = "" 
    
    for row in rows:
        cells = row.find_all("td")
        if len(cells) == 3:
            current_date = cells[0].get_text(strip=True) # get the date from the first cell
            type_cell = cells[1]
            menu_cell = cells[2]
        else:
            type_cell = cells[0]
            menu_cell = cells[1]

        # extract meal type 
        meal_type = type_cell.get_text(strip=True)

        # extract menu items 
        menu_items = [
            item.strip()
            for item in menu_cell.decode_contents().split("<br>")
            if item.strip()
        ]


        menu_text = " ".join(menu_items)

        entry = {"Date": current_date, "Menu": menu_text} # dictionary for the menu entry

        # check type of meal and append to respective list
        if '맛난' in meal_type:
            yummy.append(entry)
        elif '건강' in meal_type:
            healthy.append(entry)
    print(f"URL: {url}")
    print(f"Rows found: {len(rows)}")
    print(f"맛난: {len(yummy)} | 건강: {len(healthy)}")

    return yummy, healthy
