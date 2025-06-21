# FastAPI app instance and router inclusion

from fastapi import FastAPI
from app.api import router

app=FastAPI()

app.include_router(router)

