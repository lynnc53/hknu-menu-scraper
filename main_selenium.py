import pandas as pd 
from src.selenium_scraper import get_driver, extract_current_week, click_previous_week, extract_exam_schedule
from merge import merge_menus_and_weather
from src.add_quantity import add_quantity_to_menus
from src.clean_df import clean_df
from src.visualize import plot_top10_menus_by_quantity, plot_exam_vs_student_count, plot_rain_vs_student_count
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

def crawl_all_weeks(max_weeks=16):
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

    df_merged_yummy, df_merged_healthy = merge_menus_and_weather()
    df_merged_yummy.to_csv("data/hknu_merged_yummy_menus.csv", index=False)
    df_merged_healthy.to_csv("data/hknu_merged_healthy_menus.csv", index=False)

    df_yummy, df_healthy = add_quantity_to_menus()
    df_yummy.to_csv("data/hknu_yummy_menus_with_quantity.csv", index=False)
    df_healthy.to_csv("data/hknu_healthy_menus_with_quantity.csv", index=False)

def crawl_schedule(max_weeks=16):
    print("Crawling schedule...")
    driver = get_driver()
    driver.get("https://www.hknu.ac.kr/kor/646/subview.do")
    
    exam_schedule = []
    for _ in range(max_weeks):
        exam_schedule.extend(extract_exam_schedule(driver))
    driver.quit()
    df = pd.DataFrame(exam_schedule)
    df.to_csv("data/hknu_exam_schedule.csv", index=False)
    print("Schedule crawling complete!")

    df_healthy_cleaned, df_yummy_cleaned = clean_df()
    df_healthy_cleaned.to_csv("data/cleaned/hknu_healthy_menus_cleaned.csv", index=False)
    df_yummy_cleaned.to_csv("data/cleaned/hknu_yummy_menus_cleaned.csv", index=False)

if __name__ == "__main__":  
    # crawl_all_weeks()
    # crawl_schedule()
    plot_top10_menus_by_quantity() 
    # plot_exam_vs_student_count()
    plot_rain_vs_student_count()

    