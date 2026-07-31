#Executable code for 
#   importing in data (raw)
#   preprocessing data (clean)
#   feature creation (feat)
#   outputting data for model training

#libraries

# %%

import pandas as pd
import numpy as np
from pathlib import Path
import sys

#create a variable that gives the overall folder location
project_root = Path(__file__).resolve().parent.parent
#establish it as somewhere the executable can access other folders
sys.path.append(str(project_root))

#import source code
from source_code.data_io import load_raw_train_data, load_raw_test_data
from source_code.preprocessing import convert_numeric, convert_datetime

# from source_code.features.py 

#import in train and test
df_train = load_raw_train_data()
df_test = load_raw_test_data()

#convert dtypes

#dtype columns to convert
list_col_num = ['vendor_id', 'passenger_count', 'pickup_longitude', 'pickup_latitude', 'dropoff_longitude', 'dropoff_latitude',
                'trip_duration']
list_col_date = ['pickup_datetime', 'dropoff_datetime']

df_train = convert_numeric(df_train, list_col_num)
df_train = convert_datetime(df_train, list_col_date)

df_test = convert_numeric(df_test, list_col_num)
df_test = convert_datetime(df_test, list_col_date)


