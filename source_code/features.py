#Function code for:
#   one hot encoding
#   feature creation

import pandas as pd
import numpy as np

#convert datetime variables

def convert_hour(df_, col_):
    df_[col_+"_sin"] = np.sin(2 * np.pi * df_[col_] / 24)
    df_[col_+"_cos"] = np.cos(2 * np.pi * df_[col_] / 24)
    return df_

def convert_day_of_week(df_, col_):
    df_["day_of_week"+col_] = df_[col_].dt.dayofweek
    df_["dow_sin"+col_] = np.sin(2*np.pi*df_["day_of_week"+col_]/7)
    df_["dow_cos"+col_] = np.cos(2*np.pi*df_["day_of_week"+col_]/7)
    return df_

#longitude and latitude variables
#absolute log distance
#absolute lat distance



#calculate manhattan distance
#also calculate the log of the manhattan distance

#cluster for pick up and drop off, different number of clusters
#3 clusters for pick up and drop off, apply to training and test data

#airport indicators?

#code the store indicator as a zero or a one



