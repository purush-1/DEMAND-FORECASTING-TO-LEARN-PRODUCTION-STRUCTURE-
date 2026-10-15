from .datapipeline import rolling_features, lag_features, time_features, aggeragate, get_dummies
from .create_model import create_model
import json
import pandas as pd
from pathlib import Path

DATA_ROOT  = Path(__file__).resolve().parents[2]

data = DATA_ROOT / 'data' / 'sales_data.csv'

MODEL_ROOT = Path(__file__).resolve().parents[2]

model_path = MODEL_ROOT / 'models' / 'demand_forecasting_model.json'

def main():
    df = pd.read_csv(data)

    df = aggeragate(df)
    df = rolling_features(df)
    df = lag_features(df)
    df['Target'] = df['Quantity'].shift(-1)
    df.dropna(inplace= True)
    df = time_features(df)


    del df['Date']

    x = df.drop('Target', axis = 1)
    y = df['Target']

    model = create_model()

    model.fit(x, y)

    model.save_model(model_path)

 



if __name__  == '__main__':
    main()