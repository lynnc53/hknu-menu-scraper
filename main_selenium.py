import pandas as pd 
from src.selenium_scraper import get_driver, extract_current_week, click_previous_week

def crawl_all_weeks(max_weeks = 10):
    driver = get_driver()
    driver.get("https://www.hknu.ac.kr/kor/670/subview.do?enc=Zm5jdDF8QEB8JTJGZGlldCUyRmtvciUyRjIlMkZ2aWV3LmRvJTNGbW9uZGF5JTNEMjAyNS4wNi4yMyUyNndlZWslM0RwcmUlMjY%3D")
    all_menus = []

    for _ in range(max_weeks):
        print("scraping current week...")
        weekly_data = extract_current_week(driver)
        all_menus.extend(weekly_data)

        success = click_previous_week(driver)
        if not success:
            break

    driver.quit()
    df = pd.DataFrame(all_menus)
    df.to_csv("data/hknu_menus.csv", index=False)
    print("Scraping complete!")

if __name__ == "__main__":
    crawl_all_weeks()

    