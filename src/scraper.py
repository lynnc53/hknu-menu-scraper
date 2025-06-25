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
    res = requests.get(url,headers={"User-Agent": "Mozilla/5.0"}) # make a GET request
    soup = BeautifulSoup(res.content, "html.parser") # parse the HTML content
    rows = soup.select("table tbody tr") # select all rows in the table

    yummy, healthy = [], [] # initialize lists for yummy and healthy menus
    current_Date = "" 
    
    