from xgboost import XGBRegressor

def create_model():
    return XGBRegressor(n_estimators = 2500,
                         learning_rate = 0.005, max_depth = 5)