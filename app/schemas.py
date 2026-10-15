from pydantic import BaseModel, Field

class PredictionsResponse(BaseModel):
    Forecast : float


class PredictionsRequest(BaseModel):
    Sales : int = Field(ge = 0)
    Cost : int = Field(ge = 0)
    Profit : int = Field(ge = 0)
    Quantity : int = Field(ge = 0)
    Unit_Cost : int = Field(ge = 0)
    Unit_Price : int = Field(ge = 0)
    MA_7 : int = Field(ge = 0)
    Lag_1 : int = Field(ge = 0)
    Lag_7 : int = Field(ge = 0)
    Lag_30 : int = Field(ge = 0)
    Month : int = Field(ge = 1 , le = 12)
    Year : int = Field(ge = 2000, le = 2150)
    Quarter : int = Field(ge = 1, le = 4)
    Dayofweek : int = Field(ge = 0, le = 6)
    Dayofyear : int = Field(ge  = 1, le = 365)

