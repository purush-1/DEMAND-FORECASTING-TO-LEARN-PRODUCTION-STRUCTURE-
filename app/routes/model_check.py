from ..dependencies import get_model
from fastapi import HTTPException, APIRouter, Depends

router = APIRouter()



@router.get('/model')
def model_check(model = Depends(get_model)):
    if model is None:
        raise HTTPException(status_code= 404, detail= 'Model not found')
    
    return {'Model' : "Demand Forecasting Model",
            "Status" : "Loaded"}