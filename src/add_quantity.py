# adds student quantity from XLSX
import pandas as pd 

def add_quantity_to_menus(df, quantity_df):
    # convert all date columns to datetime format 
    quantity_df['결제일시'] = pd.to_datetime(quantity_df['결제일시']).dt.date
    df['Date'] = pd.to_datetime(df['Date']).dt.date

    # rename 식당명 to menu_type
    quantity_df.rename(columns={"식권명": "menu_type"}, inplace=True)
    quantity_df.rename(columns={"결제일시": "date"}, inplace=True)

    # filter quantity_df for relevant menu types
    df['StudentCount'] = df['Date'].apply(
        lambda date: len(quantity_df[(quantity_df['date'] == date) & 
                                    (  (quantity_df['menu_type'] == '25맛난한끼(교직원&학생)') | 
                                        (quantity_df['menu_type'] == '25맛난한끼(외부인)')
                                        )
                                    ])
    )
    return df