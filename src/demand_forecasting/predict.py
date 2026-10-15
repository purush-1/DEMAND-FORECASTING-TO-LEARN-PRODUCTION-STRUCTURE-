from .datapipeline import time_features, aggeragate, rolling_features, target_lag_features, get_dummies
import pandas as pd
from pathlib import Path

MODEL_ROOT = Path(__file__).resolve().parents[2]

model_path = MODEL_ROOT / 'models' / 'demand_forecasting_model.json'

def load_model():
    model = XGBRegressor()

    return model.load_model(model_path)

def predict(df):

    df = aggeragate(df)
    df = time_features(df)
    df = rolling_features(df)
    df = lag_features(df)
    df = get_dummies(df)

    del df['Date']

    model = load_model()

    predictions = model.predict(df)

    return predictions


