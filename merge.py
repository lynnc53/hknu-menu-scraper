import pandas as pd 
import re

def merge_menus_and_weather():
    yummy_menus = pd.read_csv("data/hknu_yummy_menus.csv")
    healthy_menus = pd.read_csv("data/hknu_healthy_menus.csv")
    weather = pd.read_csv("data/hknu_weather.csv", encoding="utf-8")

    print(weather.head())

    # rename columns for consistency 
    weather.columns = ["StationID", "StationName", "Date", "AveTemp", "Precipitation"]
    # convert Date column to datetime 
    for df in [yummy_menus, healthy_menus]:
        # Extract just the date part like "2025.06.16" from "2025.06.16( 월 )"
        df["Date"] = df["Date"].astype(str).str.extract(r"(\d{4}\.\d{2}\.\d{2})")[0]
        df["Date"] = pd.to_datetime(df["Date"], format="%Y.%m.%d")
    weather["Date"] = pd.to_datetime(weather["Date"])
    # adding a columns of rain 
    weather["Precipitation"] = weather["Precipitation"].fillna(0)
    weather["Rain"] = weather["Precipitation"].apply(lambda x: 1 if x > 0 else 0)

    # convert Date column to datetime in yummy_menus and healthy_menus
    yummy_menus["Date"] = pd.to_datetime(yummy_menus["Date"])
    healthy_menus["Date"] = pd.to_datetime(healthy_menus["Date"])

    # merge yummy_menus and weather on Date
    merged_yummy = pd.merge(yummy_menus, weather, on="Date", how="left")
    # merge healthy_menus and weather on Date
    merged_healthy = pd.merge(healthy_menus, weather, on="Date", how="left")

    return merged_yummy, merged_healthy

    # print(merged_yummy.head())
    # print(merged_healthy.head())

    # merged_yummy.to_csv("data/merged_yummy_menus.csv", index=False)
    # merged_healthy.to_csv("data/merged_healthy_menus.csv", index=False) 