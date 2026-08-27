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

#NULLS
#   there are no nulls in the data

#DUPLICATES
#   the variable 'id' is distinct in both train and test data
#   by all variables (excluding 'id' and 'vendor_id') there is 1 duplicate row in test
#   by all variables (excluding 'id', 'vendor_id' and target variables) there are 7 duplicates in train
#   going to leave these in since they have different 'id' numbers

#COLUMN CHECK
#trip_duration is calculated as (dropoff_datetime - pickup_datetime) in seconds

#DATA CLEANING

# - remove instances where passenger count is 0 (60 instances)
# - remove instances where the trip_duration is less than 1 minute and more than 4 hours.
# - remove instances where the pickup and dropoff location is the same but the trip_duration is more than 15 minutes
# - remove instances where the longitude and latitude are outside of NYC and the suburb area

def clean_data(df_):
    """
    - removes instances where passenger count is 60
    - removes instances where trip duration is less than 1 min or more than 4 hours
    - remove instances where the pickup and dropoff location is the same but the trip_duration is more than 15 minutes
    - remove instances where the longitude and latitude are outside of NYC and the suburb area
    """

    #removes instances where passenger count is 0
    mask_passenger_count = (df_['passenger_count']>0)

    #removes instances where the trip duration is less than a min, more than 4 hours
    MIN_DURATION = 60
    MAX_DURATION = 14400
    mask_duration = (df_['trip_duration'].between(MIN_DURATION, MAX_DURATION))

    #removes instances where pickup/dropoff is the same and the trip is more than 15 min
    mask_same_loc = (
            (df_['pickup_longitude']==df_['dropoff_longitude']) &
            (df_['pickup_latitude']==df_['dropoff_latitude']) &
            (df_['trip_duration']>900)
            )

    #removes instances where the trip is outside NYC
    MIN_LONGITUDE = -74.30
    MAX_LONGITUDE = -73.60

    MIN_LATITUDE = 40.45
    MAX_LATITUDE = 41.00

    mask_range = (
        df_['pickup_longitude'].between(MIN_LONGITUDE, MAX_LONGITUDE) &
        df_['dropoff_longitude'].between(MIN_LONGITUDE, MAX_LONGITUDE) &
        df_['pickup_latitude'].between(MIN_LATITUDE, MAX_LATITUDE) &
        df_['dropoff_latitude'].between(MIN_LATITUDE, MAX_LATITUDE)
        )

    df_ = df_[mask_passenger_count & mask_duration & mask_range].copy()
    df_ = df_[~mask_same_loc].copy()
    df_.reset_index(drop = True, inplace = True)

    return df_
