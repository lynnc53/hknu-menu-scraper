import pandas as pd 

# import all required dataframes 
df_yummy = pd.read_csv("data/merged_yummy_menus.csv")
df_healthy = pd.read_csv("data/merged_healthy_menus.csv")
df_students = pd.read_excel("cost_data.xlsx", sheet_name="결제정보")

# convert all date columns to datetime format 
df_students['결제일시'] = pd.to_datetime(df_students['결제일시']).dt.date
df_yummy['Date'] = pd.to_datetime(df_yummy['Date']).dt.date
df_healthy['Date'] = pd.to_datetime(df_healthy['Date']).dt.date

# rename 식당명 to menu_type
df_students.rename(columns={"식권명": "menu_type"}, inplace=True)
df_students.rename(columns={"결제일시": "date"}, inplace=True)

# checking unique menu types in df_students 
print(df_students['menu_type'].unique())

# # for each date, calculate the number of students who ordered each menu type
# for date in df_yummy['Date']:
#     cnt = 0 
#     for date2 in df_students['결제일시']:
#         if date == date2:
#             cnt += 1
#     df_yummy['StudentCount'] = cnt

# for date in df_healthy['Date']:
#     cnt = 0 
#     for date2 in df_students['결제일시']:
#         if date == date2:
#             cnt += 1
#     df_healthy['StudentCount'] = cnt

# # count the number of students for 맛난한끼
# num_students_yummy = len(df_students[df_students['menu_type'] == '25맛난한끼(교직원&학생)'])

# # count the number of students for 건강한끼
# num_students_healthy = len(df_students[df_students['menu_type'] == '25건강한끼(교직원&학생)'])]

# for date in df_yummy['Date']:
#     df_yummy['StudentCount'] = len(df_students[df_students['결제일시'] == date & df_students['menu_type'] == '25맛난한끼(교직원&학생)'])

# for date in df_healthy['Date']:
#     df_healthy['StudentCount'] = len(df_students[df_students['결제일시'] == date & df_students['menu_type'] == '25건강한끼(교직원&학생)'])

# For yummy menus
df_yummy['StudentCount'] = df_yummy['Date'].apply(
    lambda date: len(df_students[(df_students['date'] == date) & 
                                 (  (df_students['menu_type'] == '25맛난한끼(교직원&학생)') | 
                                    (df_students['menu_type'] == '25맛난한끼(외부인)')
                                    )
                                ])
)

# For healthy menus
df_healthy['StudentCount'] = df_healthy['Date'].apply(
    lambda date: len(df_students[(df_students['date'] == date) & 
                                 (
                                    (df_students['menu_type'] == '25건강한끼(교직원&학생)') |
                                    (df_students['menu_type'] == '25건강한끼(외부인)')
                                    )
                                ])
)

print(df_yummy.head())

df = pd.DataFrame(df_yummy)
df.to_csv("data/yummy+weather+students.csv", index=False)

df = pd.DataFrame(df_healthy)
df.to_csv("data/healthy+weather+students.csv", index=False)