import pandas as pd 

def time_features(df):
    df = df.copy()
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date')

    df['Month'] = df['Date'].dt.month
    df['Year'] = df['Date'].dt.year
    df['Quarter'] = df['Date'].dt.year
    df['Dayofweek'] = df['Date'].dt.dayofweek
    df['Dayofyear'] = df['Date'].dt.dayofyear
    return df

def aggeragate(df):
    df = df.copy()

    return df.groupby('Date').agg(Sales = ('Revenue', 'sum'),
                            Cost = ('Cost', 'sum'),
                                       Profit = ('Profit', 'sum'),
                                        Quantity = ('Order_Quantity', 'sum'),
                                         Unit_Cost = ('Unit_Cost', 'sum'),
                                          Unit_Price = ('Unit_Price', 'sum')).reset_index()

def lag_features(df):
    df = df.copy()
    
    df['Lag_1'] = df['Quantity'].shift(1)
    df['Lag_7'] = df['Quantity'].shift(7)
    df['Lag_30'] = df['Quantity'].shift(30)

    df.dropna(inplace = True)

    return df

def rolling_features(df):
    df = df.copy()


    df['MA_7'] = df['Quantity'].shift(1).rolling(7).mean()

    df.dropna(inplace = True)
    return df

def get_dummies(df):

    df = pd.get_dummies(df, columns= ['Product'], prefix= 'Product')

    

    return df