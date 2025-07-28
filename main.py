import pandas as pd 
from src.scraper import get_driver, extract_current_week, click_previous_week, extract_exam_schedule
from src.merger import merge_menus_and_weather
from src.add_quantity import add_quantity_to_menus
from src.cleaner import clean_df
#from src.visualize import plot_top10_menus_by_quantity, plot_exam_vs_student_count, plot_rain_vs_student_count
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

def crawl_all_weeks(max_weeks=5):
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
    # convert lists to DataFrames
    healthy_df = pd.DataFrame(all_healthy_menus)
    yummy_df = pd.DataFrame(all_yummy_menus)
    weather_df = pd.read_csv("data/raw/hknu_weather.csv", encoding="euc-kr")

    # calling merger.py to merge menus and weather data 
    merged_healthy_df = merge_menus_and_weather(healthy_df, weather_df)
    merged_yummy_df = merge_menus_and_weather(yummy_df, weather_df)

    # calling add_quantity.py to add student quantity to dataframes 
    quantity_df = pd.read_excel("data/raw/cost_data.xlsx", sheet_name="결제정보")
    quantity_df.columns = quantity_df.columns.str.strip().str.replace(r"\s+", "", regex=True)

    print(quantity_df.columns.tolist())
    print(quantity_df.head())
    yummy_df = add_quantity_to_menus(merged_yummy_df, quantity_df)
    healthy_df = add_quantity_to_menus(merged_healthy_df, quantity_df)

    # save the final dataframes to csv files 
    yummy_df.to_csv("data/cleaned/yummy_menus_with_weather_and_quantity.csv", index=False)
    healthy_df.to_csv("data/cleaned/healthy_menus_with_weather_and_quantity.csv", index=False)

def crawl_schedule(max_weeks=5):
    print("Crawling schedule...")
    driver = get_driver()
    driver.get("https://www.hknu.ac.kr/kor/646/subview.do")
    
    exam_schedule = []
    for _ in range(max_weeks):
        exam_schedule.extend(extract_exam_schedule(driver))
    driver.quit()

    # calling utils.py and scraper.py to extract exam content 
    schedule_df = pd.DataFrame(exam_schedule)
    print("Schedule crawling complete!")

    # calling cleaner.py to clean the exam schedule data
    yummy_df = pd.read_csv("data/cleaned/yummy_menus_with_weather_and_quantity.csv")
    healthy_df = pd.read_csv("data/cleaned/healthy_menus_with_weather_and_quantity.csv")

    healthy_cleaned = clean_df(healthy_df, schedule_df)
    yummy_cleaned = clean_df(yummy_df, schedule_df)

    healthy_cleaned.to_csv("data/cleaned/healthy_menus_cleaned.csv", index=False)
    yummy_cleaned.to_csv("data/cleaned/yummy_menus_cleaned.csv", index=False)

if __name__ == "__main__":  
    crawl_all_weeks()
    crawl_schedule()
    # plot_top10_menus_by_quantity() 
    # plot_exam_vs_student_count()
    # plot_rain_vs_student_count()

    