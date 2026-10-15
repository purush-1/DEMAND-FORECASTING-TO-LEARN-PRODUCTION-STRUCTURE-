from demand_forecasting.datapipeline import rolling_features, lag_features
import pandas as pd


def test_lag_features():
    df = pd.DataFrame({'Quantity' : range(1, 1001)
                       })

    result = lag_features(df)

    assert result.loc[30, 'Lag_7'] == 24
    assert result.loc[30, 'Lag_1'] == 30
    assert result.loc[30, 'Lag_30'] == 1
   

    print("HEAD",result.head())
    print("INDEX",result.index)

def test_rolling_features():
    df = pd.DataFrame({'Quantity' : range(1, 1001)
                       })

    result = rolling_features(df)


    assert result.loc[7, 'MA_7'] == 4
    assert result.loc[8, 'MA_7'] == 5
