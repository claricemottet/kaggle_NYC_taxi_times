#Function code for:
#   dtypes
#   handling nulls

import pandas as pd

#dtype conversion functions
def convert_numeric(df_, list_col_num):
    list_convert_num = [x for x in list_col_num if x in df_.columns]
    df_[list_convert_num] = df_[list_convert_num].apply(pd.to_numeric)
    return df_

def convert_datetime(df_, list_col_date):
    list_convert_date = [x for x in list_col_date if x in df_.columns]
    df_[list_convert_date] = df_[list_convert_date].apply(pd.to_datetime)
    return df_


