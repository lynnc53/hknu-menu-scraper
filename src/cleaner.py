# column renaiming and exam flag logic 
import pandas as pd 

def clean_df(df, schedule_df):
    # rename columns for clarity
    df['날짜'] = df['Date']
    df['요일'] = df['Date'].apply(lambda x: pd.to_datetime(x).day_name())
    df['시간대'] = "점심"
    df['메뉴'] = df['Main Menu']
    df['기온'] = df['AveTemp']
    df['강수량'] = df['Precipitation']
    df['식수량'] = df['StudentCount']

    # order dates 
    df.sort_values(by='날짜', ascending=True, inplace=True)

    # 1. Ensure 'Date' is datetime.date
    schedule_df['Date'] = pd.to_datetime(schedule_df['Date']).dt.date

    # 2. Initialize 시험여부 column
    schedule_df['시험여부'] = '아니오'

    # 3. Build a set for quick existence check and a list to store new rows
    existing_dates = set(schedule_df['Date'])
    new_rows = []

    for index, row in schedule_df.iterrows():
        exam_date = row['Date']
        if "시험" in row['Content']:
            for i in range(7):  # current + next 6 days
                future_date = exam_date + pd.Timedelta(days=i)
                if future_date in existing_dates:
                    # Update 시험여부 if date exists
                    schedule_df.loc[schedule_df['Date'] == future_date, '시험여부'] = '예'
                else:
                    # Add new row
                    new_rows.append({'Date': future_date, 'Content': '', '시험여부': '예'})
                    existing_dates.add(future_date)

    # 4. Append new rows if any
    if new_rows:
        schedule_df = pd.concat([schedule_df, pd.DataFrame(new_rows)], ignore_index=True)

    # 5. Recreate lookup dictionary
    exam_dict = dict(zip(schedule_df['Date'], schedule_df['시험여부']))

    # 6. Function to lookup 시험여부 based on date
    def check_exam(date):
        date = pd.to_datetime(date).date()  # Ensure date type matches
        return exam_dict.get(date, '아니오')  # default to '아니오' if not found

    # 7. Apply to both healthy and yummy DataFrames
    df['시험기간 여부'] = df['날짜'].apply(check_exam)

    # remove all rows with '식수량' less than 10
    df = df[df['식수량'] > 10]

    return df
