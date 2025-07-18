import pandas as pd 

def clean_df():
    # import all require dataframes
    df_healthy = pd.read_csv("data/hknu_healthy_menus_with_quantity.csv")
    df_yummy = pd.read_csv("data/hknu_yummy_menus_with_quantity.csv")
    df_schedule = pd.read_csv("data/hknu_exam_schedule.csv")

    # declare empty dataframes to store cleaned data 
    df_healthy_cleaned = pd.DataFrame()
    df_yummy_cleaned = pd.DataFrame()   

    # columns: 날짜 요일, 시간대, 메뉴, 기온, 강수량, 시험기간 여부, 학기 중 여부, 식수량 
    df_healthy_cleaned['날짜'] = df_healthy['Date']
    df_healthy_cleaned['요일'] = df_healthy['Date'].apply(lambda x: pd.to_datetime(x).day_name())
    df_healthy_cleaned['시간대'] = "점심"
    df_healthy_cleaned['메뉴'] = df_healthy['Main Menu']
    df_healthy_cleaned['기온'] = df_healthy['AveTemp']
    df_healthy_cleaned['강수량'] = df_healthy['Precipitation']
    df_healthy_cleaned['식수량'] = df_healthy['StudentCount']

    df_yummy_cleaned['날짜'] = df_yummy['Date']
    df_yummy_cleaned['요일'] = df_yummy['Date'].apply(lambda x: pd.to_datetime(x).day_name())
    df_yummy_cleaned['시간대'] = "점심"
    df_yummy_cleaned['메뉴'] = df_yummy['Main Menu']
    df_yummy_cleaned['기온'] = df_yummy['AveTemp']
    df_yummy_cleaned['강수량'] = df_yummy['Precipitation']
    df_yummy_cleaned['식수량'] = df_yummy['StudentCount']

    # order dates 
    df_healthy_cleaned.sort_values(by='날짜', ascending=True, inplace=True)
    df_yummy_cleaned.sort_values(by='날짜', ascending=True, inplace=True)

    # 1. Ensure 'Date' is datetime.date
    df_schedule['Date'] = pd.to_datetime(df_schedule['Date']).dt.date

    # 2. Initialize 시험여부 column
    df_schedule['시험여부'] = '아니오'

    # 3. Build a set for quick existence check and a list to store new rows
    existing_dates = set(df_schedule['Date'])
    new_rows = []

    for index, row in df_schedule.iterrows():
        exam_date = row['Date']
        if "시험" in row['Content']:
            for i in range(7):  # current + next 6 days
                future_date = exam_date + pd.Timedelta(days=i)
                if future_date in existing_dates:
                    # Update 시험여부 if date exists
                    df_schedule.loc[df_schedule['Date'] == future_date, '시험여부'] = '예'
                else:
                    # Add new row
                    new_rows.append({'Date': future_date, 'Content': '', '시험여부': '예'})
                    existing_dates.add(future_date)

    # 4. Append new rows if any
    if new_rows:
        df_schedule = pd.concat([df_schedule, pd.DataFrame(new_rows)], ignore_index=True)

    # 5. Recreate lookup dictionary
    exam_dict = dict(zip(df_schedule['Date'], df_schedule['시험여부']))
    # 4. Function to lookup 시험여부 based on date
    def check_exam(date):
        date = pd.to_datetime(date).date()  # Ensure date type matches
        return exam_dict.get(date, '아니오')  # default to '아니오' if not found

    # 5. Apply to both healthy and yummy DataFrames
    df_healthy_cleaned['시험기간 여부'] = df_healthy_cleaned['날짜'].apply(check_exam)
    df_yummy_cleaned['시험기간 여부'] = df_yummy_cleaned['날짜'].apply(check_exam)

    # remove all rows with '식수량' less than 10
    df_healthy_cleaned = df_healthy_cleaned[df_healthy_cleaned['식수량'] > 10]
    df_yummy_cleaned = df_yummy_cleaned[df_yummy_cleaned['식수량'] > 10]

    return df_healthy_cleaned, df_yummy_cleaned
