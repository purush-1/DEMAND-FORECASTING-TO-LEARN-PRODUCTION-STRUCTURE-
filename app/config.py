from pathlib import Path
import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    model_name : str = 'demand_forecasting_model.json'

    @property
    def model_path(self) -> Path:
        model_root = Path(__file__).resolve().parents[1]
        return model_root / 'models' / self.model_name

settings = Settings()