# NYC Taxi Trip Duration

Predicting how long a New York City taxi ride will take, using only what is known at pickup: time, pickup and dropoff coordinates, passenger count and vendor. This is my solution to Kaggle's [NYC Taxi Trip Duration](https://www.kaggle.com/competitions/nyc-taxi-trip-duration) competition, which is scored on Root Mean Squared Log Error (RMSLE).

**Best result:** XGBoost, with an RMSLE of **0.3312** on validation and **0.39782** on Kaggle.

| Model | Validation RMSLE | Validation RMSE (seconds) | Validation R² | Kaggle RMSLE |
|---|---|---|---|---|
| Linear Regression | 0.4437 | 418.50 | 0.6549 | 0.50266 |
| LASSO | 0.4437 | 417.36 | 0.6549 | 0.50303 |
| Ridge | 0.4437 | 418.48 | 0.6549 | 0.50265 |
| Random Forest | 0.3503 | 300.64 | 0.7850 | 0.42637 |
| **XGBoost** | **0.3312** | **284.58** | **0.8078** | **0.39782** |

RMSLE and RMSE are calculated on trip duration in seconds. R² is calculated on the log scale.

## Key findings

- **The linear models underfit.** All three scored the same RMSLE and the best regularization strengths were small, so regularization made no difference. Trip duration doesn't change linearly with the features: the effect of distance depends on time of day and location.
- **Tree models capture those interactions.** Random Forest lowered RMSLE by about 21% compared to the linear models. XGBoost lowered it by about 25%, and by about 5% compared to Random Forest.
- **Distance matters most.** `haversine_distance` accounts for 53% of XGBoost's total gain, followed by `is_weekend` (8%) and hour of day (9% across the sine and cosine features). Pickup and dropoff coordinates contribute 3–4% each, likely capturing neighborhood and traffic effects.
- **Data cleaning thresholds helped.** Experimenting with the minimum and maximum trip durations improved the models. The choice of haversine or Manhattan distance, and log or non-log, had a milder effect.

Validation scores are better than Kaggle scores for every model. A likely reason is that outliers were removed from the training and validation data, while the test set has to be predicted in full.

## Data

The dataset has 1,458,644 training rows and 625,134 test rows, covering taxi trips from January through June 2016. Train and test share the same columns, except that `dropoff_datetime` and `trip_duration` appear only in train. `trip_duration`, in seconds, is the target.

The raw files are too large for git. To download them, accept the competition rules on Kaggle, then place the CSVs in `data/raw/`:

```bash
kaggle competitions download -c nyc-taxi-trip-duration -p data/raw
unzip 'data/raw/*.zip' -d data/raw
```

If the download contains nested zips, unzip those as well. You should end up with `train.csv`, `test.csv` and `sample_submission.csv`.

## Approach

### Cleaning

The data has no nulls and no duplicate `id` values. Seven training rows match on every other column; these were kept because their IDs differ. Cleaning applies to the training set only and removes 4,729 rows (0.3%), leaving 1,453,915:

- trips with zero passengers
- trips shorter than 10 seconds or longer than 3 hours
- trips that start or end outside the NYC area (longitude -74.30 to -73.60, latitude 40.45 to 41.00)

### Features

Each model uses 16 features:

| Group | Features |
|---|---|
| Distance | `haversine_distance` for tree models, `log_haversine_distance` for linear models |
| Location | pickup and dropoff latitude and longitude |
| Time | sine and cosine of hour, day of week and month; `is_weekend` |
| Other | `passenger_count`, `store_and_fwd_flag_ind`, `vendor_id_1`, `vendor_id_2` |

Manhattan distance and bearing were also engineered and explored, but they aren't in the final feature set.

### Modeling

- **Target:** `log_trip_duration`, because raw duration is heavily skewed. Predictions are converted back to seconds with `expm1`.
- **Validation:** a random 80/20 split of the cleaned training data, with seed 42 and standard-scaled features.
- **Tuning:** LASSO and Ridge pick their alpha with 5-fold cross-validation. Random Forest and XGBoost were tuned by hand across runs.
- **Tracking:** parameters, metrics and models are logged to MLflow. The notebook includes `check_previous_run()`, which warns before retraining with parameters that have already been tried.

## Project structure

```
├── notebooks/
│   ├── nyc_taxi_times.ipynb      # Main notebook: cleaning through final results
│   └── data_exploration.ipynb    # Detailed EDA behind the cleaning and feature decisions
├── outputs/                      # Kaggle submission files, one per model
├── source_code/                  # Early pipeline modules (see note below)
├── exe_scripts/prepare_data.py   # Early pipeline script (see note below)
└── data/raw/                     # Kaggle CSVs (not tracked in git)
```

`notebooks/nyc_taxi_times.ipynb` is the source of truth and is self-contained. The `source_code/` modules and `exe_scripts/prepare_data.py` are an earlier refactor that the notebook doesn't import. They still use the older cleaning rules (60 seconds to 4 hours, plus removing same-location trips over 15 minutes), and the script doesn't save its output. `outputs/df_test_eval.csv` is also an earlier submission; the current notebook writes the `df_test_eval_<model>.csv` files.

## Running it

Developed on Python 3.12 with these library versions:

```bash
pip install pandas==2.2.2 numpy==2.1.1 scikit-learn==1.5.2 xgboost==2.1.1 \
    mlflow==3.17.2 matplotlib==3.9.2 seaborn==0.13.2 jupyter
```

Run `notebooks/nyc_taxi_times.ipynb` from top to bottom with `notebooks/` as the working directory, since paths are resolved from there. Each model writes its predictions to `outputs/`.

**To reproduce the linear model scores,** swap `haversine_distance` for the commented-out `log_haversine_distance` in the feature list first. The notebook is currently set up for the tree models, and linear regression scores 0.5442 with raw distance rather than 0.4437. T


## Author

Clarice Mottet
