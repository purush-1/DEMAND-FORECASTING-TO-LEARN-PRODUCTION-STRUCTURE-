from fastapi import FastAPI
import time 
import logging
from .routes.health import router as health_router
from .routes.model_check import router as model_check_router
from .routes.predict import router as predict_router

logging.basicConfig(level= logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.include_router(health_router)
app.include_router(model_check_router)
app.include_router(predict_router, prefix= '/api v1/ predict')


@app.middleware('http')
async def timer(request, 
                call_next):

    start = time.time()

    response = await call_next(request)

    end = time.time()

    logger.info('%s %s took %.4f seconds',
                request.method,
                request.url,
                end - start)

    return response








