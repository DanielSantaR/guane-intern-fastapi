from fastapi import APIRouter
#from app.api.endpoints import dog
from app.sql_app import endpoints

api_router = APIRouter()
api_router.include_router(endpoints.router, prefix='/dogs', tags=['dogs'])