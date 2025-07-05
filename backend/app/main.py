# FastAPI app instance and router inclusion

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import router

from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Allow NGINX and local requests
origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api", tags=["API"])
