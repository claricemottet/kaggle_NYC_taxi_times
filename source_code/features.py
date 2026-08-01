#Function code for:
#   one hot encoding
#   feature creation

import pandas as pd
import numpy as np

#convert datetime variables

def convert_hour(df_, col_):
    df_["hour_"+col_] = df_[col_].dt.hour
    df_["hour_sin_"+col_] = np.sin(2 * np.pi * df_["hour_"+col_] / 24)
    df_["hour_cos_"+col_] = np.cos(2 * np.pi * df_["hour_"+col_] / 24)
    return df_

def convert_day_of_week(df_, col_):
    df_["dow_"+col_] = df_[col_].dt.dayofweek
    df_["dow_sin"+col_] = np.sin(2*np.pi*df_["dow_"+col_]/7)
    df_["dow_cos"+col_] = np.cos(2*np.pi*df_["dow_"+col_]/7)
    return df_

def convert_month(df_, col_):
    df_["month_"+col_] = df_[col_].dt.month
    df_["month_sin"+col_] = np.sin(2*np.pi*df_["month_"+col_]/12)
    df_["month_cos"+col_] = np.cos(2*np.pi*df_["month_"+col_]/12)
    return df_


#longitude and latitude variables
#absolute log distance
#absolute lat distance

#calculate manhattan distance
#also calculate the log of the manhattan distance

def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371  # earth radius in km
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    c = 2 * np.arcsin(np.sqrt(a))
    return R * c

def calc_manhattan_distance(df_):
    df_["manhattan_distance"] = (
        haversine_distance(df_["pickup_latitude"], df_["pickup_longitude"], df_["pickup_latitude"], df_["dropoff_longitude"])
        + haversine_distance(df_["pickup_latitude"], df_["dropoff_longitude"], df_["dropoff_latitude"], df_["dropoff_longitude"])
    )
    df_["manhattan_distance_log"] = np.log1p(df_["manhattan_distance"])
    return df_

#calculate havershine distance
#also calc log

def calc_haversine_distance(df_):
    df_["haversine_distance"] = haversine_distance(
        df_["pickup_latitude"], df_["pickup_longitude"], df_["dropoff_latitude"], df_["dropoff_longitude"]
    )
    df_["haversine_distance_log"] = np.log1p(df_["haversine_distance"])
    return df_

#calculate bearing (direction of trip, cyclical)


#cluster for pick up and drop off, different number of clusters
#3 clusters for pick up and drop off, apply to training and test data

#airport indicators?

#code the store indicator as a zero or a one

#is a weekend indicator

#same_pickup_dropoff_location



