from fastapi import APIRouter, HTTPException
from app.services.weather import WeatherService

router = APIRouter()
weather_service = WeatherService()

@router.get("/hello")
async def get_hello():
	try:
		return {"message": "Hello, World!"}
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))