# HKNU Menu Scraper 
This project uses Selenium and BeautifulSoup to scrape weekly cafeteria menus from the Hankyong National University (HKNU) website. The scraper collects both 맛난한끼 and 건강한 meals ad saves the data to a csv file.

## 1. Clone the Repository 
```bash
git clone https://github.com/your-username/hknu-menu-scraper.git
cd hknu-menu-scraper
```

## 2. Run the Scraper
```bash
python main_selenium.py
```
This will scrape up to 10 weeks of menu data by default and save it in the data/hknu_menus.csv file

## 3. Optional: Scrape More Weeks
By default, the scraper goes back to only 10 weeks.
To change this, open main_selenium.py and update:
```python
crawl_all_weeks(max_weeks=10)
```
Change 10 to any number of weeks you want to go back

## Notes
* works best with Chrome installed
* install the following libraries: selenium, beautifulsoup4, webdriver-manager, pandas
