from time import time
from fastapi import APIRouter

router = APIRouter()

@router.middleware('http')
async def timer(request, 
                call_next):

    start = time.time()

    response = await call_next(request)

    end = time.time()

    print (f'{request.method} {request.url} took {end - start :.4f} seconds')

    return response