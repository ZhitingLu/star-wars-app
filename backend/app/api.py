# API router, endpoints

from fastapi import APIRouter

router = APIRouter()

BASE_SWAPI_URL = "https://swapi.dev/api"

@router.get("/")
async def read_root():
    return {"message": "Welcome, Star Wars fans!"}

