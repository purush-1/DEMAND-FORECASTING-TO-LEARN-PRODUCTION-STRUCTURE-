import pandas as pd
from ..dependencies import get_model
from fastapi import APIRouter, Depends, HTTPException
import logging
from ..schemas import PredictionsRequest, PredictionsResponse
from demand_forecasting.datapipeline import rolling_features, lag_features

router = APIRouter()

logger = logging.getLogger(__name__)

@router.post('/Predict', response_model= PredictionsResponse)
def make_prediction(request : PredictionsRequest, model = Depends(get_model)):

    df = pd.DataFrame([request.model_dump()])


    try:
        predictions = model.predict(df)

    except Exception:

        logger.exception("Prediction Failed")
        raise HTTPException(status_code= 500, detail= 'Prediction Failed')

    
    return {'Forecast' : predictions[0]}