from xgboost import XGBRegressor
from .config import settings


def load_the_model():
    model = XGBRegressor() 

    model.load_model(settings.model_path)

    return model