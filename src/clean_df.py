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

    # 1. Ensure exam schedule dates are datetime.date
    df_schedule['Date'] = pd.to_datetime(df_schedule['Date']).dt.date

    # 2. Mark '예' if "시험" is in the content
    df_schedule['시험여부'] = df_schedule['Content'].apply(lambda x: '예' if "시험" in x else '아니오')

    # 3. Create a dictionary {date: '예' or '아니오'} for fast lookup
    exam_dict = dict(zip(df_schedule['Date'], df_schedule['시험여부']))
    print(exam_dict)

    # 4. Function to lookup 시험여부 based on date
    def check_exam(date):
        date = pd.to_datetime(date).date()  # Ensure date type matches
        return exam_dict.get(date, '아니오')  # default to '아니오' if not found

    # 5. Apply to both healthy and yummy DataFrames
    df_healthy_cleaned['시험기간 여부'] = df_healthy_cleaned['날짜'].apply(check_exam)
    df_yummy_cleaned['시험기간 여부'] = df_yummy_cleaned['날짜'].apply(check_exam)


    return df_healthy_cleaned, df_yummy_cleaned
