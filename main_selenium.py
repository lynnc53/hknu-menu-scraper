import pandas as pd 
from src.s_scraper import get_driver, extract_current_week, click_previous_week
# note: change max_weeks if you want to scrape more than 10 weeks
# def crawl_all_weeks(max_weeks = 10):
#     driver = get_driver() # function to initialize the selenium  webdriver 
#     driver.get("https://www.hknu.ac.kr/kor/670/subview.do?enc=Zm5jdDF8QEB8JTJGZGlldCUyRmtvciUyRjIlMkZ2aWV3LmRvJTNGbW9uZGF5JTNEMjAyNS4wNi4yMyUyNndlZWslM0RwcmUlMjY%3D")
#     all_menus = []

#     for _ in range(max_weeks):
#         print("scraping current week...")
#         weekly_data = extract_current_week(driver)
#         all_menus.extend(weekly_data)

#         success = click_previous_week(driver)
#         if not success:
#             break

#     driver.quit()
#     df = pd.DataFrame(all_menus)
#     df.to_csv("data/hknu_menus.csv", index=False)
#     print("Scraping complete!")

def crawl_all_weeks(max_weeks=15):
    driver = get_driver()
    driver.get("https://www.hknu.ac.kr/kor/670/subview.do?enc=Zm5jdDF8QEB8JTJGZGlldCUyRmtvciUyRjIlMkZ2aWV3LmRvJTNGbW9uZGF5JTNEMjAyNS4wNi4yMyUyNndlZWslM0RwcmUlMjY%3D")
    all_yummy_menus = []
    all_healthy_menus = []

    for _ in range(max_weeks):
        print("Scraping current week...")
        yummy_menus, healthy_menus = extract_current_week(driver)
        all_yummy_menus.extend(yummy_menus)
        all_healthy_menus.extend(healthy_menus)

        success = click_previous_week(driver)
        if not success:
            break
    
    driver.quit()
    df = pd.DataFrame(all_yummy_menus)
    df.to_csv("data/hknu_yummy_menus.csv", index=False)
    print("Yummy menus scraping complete!")
    df = pd.DataFrame(all_healthy_menus)
    df.to_csv("data/hknu_healthy_menus.csv", index=False)
    print("Healthy menus scraping complete!")

if __name__ == "__main__":  
    crawl_all_weeks()

    