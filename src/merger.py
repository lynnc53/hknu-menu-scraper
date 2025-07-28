# merging weather and food data
import pandas as pd 
import re

def merge_menus_and_weather(menu_df, weather_df):
    # Ensure the weather DataFrame has the correct columns
    weather_df = weather_df[["지점", "지점명", "일시", "평균기온(°C)", "일강수량(mm)"]]
    weather_df.columns = ["StationID", "StationName", "Date", "AveTemp", "Precipitation"]

    weather_df["Date"] = pd.to_datetime(weather_df["Date"], format="%Y-%m-%d")
    weather_df["Precipitation"] = weather_df["Precipitation"].fillna(0)
    weather_df["Rain"] = weather_df["Precipitation"].apply(lambda x: 1 if x > 0 else 0)

    menu_df["Date"] = menu_df["Date"].astype(str).str.extract(r"(\d{4}\.\d{2}\.\d{2})")[0]
    menu_df["Date"] = pd.to_datetime(menu_df["Date"], format="%Y.%m.%d")
    
    merged_df = pd.merge(menu_df, weather_df, on="Date", how="left")

    return merged_df 


