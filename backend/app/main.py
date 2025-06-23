# FastAPI app instance and router inclusion

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import router

app = FastAPI(
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Allow NGINX, Docker, and local requests
origins = [
    "http://localhost:6969",
    "http://localhost:3000",
    "http://starwars-nginx",
    "http://starwars-frontend",
    "http://127.0.0.1:6969"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Or use ["*"] for open dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api", tags=["API"])
