# this function will be used to loop backward in time, 7 days at a time 
import pandas as pd
from datetime import datetime, timedelta
from src.scraper import scrape_week 

def crawl_all(start_date='2025-06-23'):
    current = datetime.strptime(start_date, '%Y-%m-%d')
    yummy_all = []
    healthy_all = []

    while True:
        date_str = current.strftime('%Y.%m.%d')     
        print(f"Scraping {date_str}... ")
        yummy, healthy = scrape_week(date_str)

        if not yummy and not healthy:
            print("No more data to scrape. Stopping.")
            break
        
        yummy_all.extend(yummy)
        healthy_all.extend(healthy) # using extend not append to flatten the list 
        # extend is used when you want to add elements of an iterable (like a list) to another list

        current -=timedelta(days=7)  # go back one week
        # timedelta is used to represent a duration, the difference between two dates or times
        
    # Save as CSV
    pd.DataFrame(yummy_all).to_csv("data/matnan.csv", index=False)
    pd.DataFrame(healthy_all).to_csv("data/geongang.csv", index=False)

if __name__ == "__main__":
    crawl_all()