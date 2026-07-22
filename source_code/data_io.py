
#Function code for
#   libraries
#   establishing filepaths
#   data input/output (load, save)


#libraries

import pandas as pd
import numpy as np
import os
from pathlib import Path

#path variables
project_root = Path.cwd().parent

raw_path = project_root / "data" / "raw"
clean_path = project_root / "data" / "clean"

#load raw functions
def load_raw_train_data():
    return pd.read_csv(raw_path / "train.csv", dtype = str)

def load_raw_test_data():
    return pd.read_csv(raw_path / "test.csv", dtype = str)

def load_raw_sample_data():
    return pd.read_csv(raw_path / "sample_submission.csv", dtype = str)

# #save clean functions
# def save_clean_train(df, filename):
#     return 

# load clean functions