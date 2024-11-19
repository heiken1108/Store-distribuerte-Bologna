from fastapi import APIRouter, HTTPException
from app.services.weather import WeatherService
from datetime import date, datetime, timedelta

router = APIRouter()
weather_service = WeatherService()


@router.get("/weather/{city}")
async def get_weather(city: str, end_datetime: datetime = None):
	if end_datetime is None:
		end_datetime = datetime.now() + timedelta(days=9)
	end_date = end_datetime.date()
	try:
		current = weather_service.get_current_weather(city)
		daily = weather_service.get_forecast_daily(city, end_date)
		hourly = weather_service.get_forecast_hourly(city, end_datetime)
		daily_forecasts = make_daily_forecasts(daily)
		hourly_forecasts = make_hourly_forecasts(hourly)
		data = {
			'Location': city,
			'Local time': current['location']['localtime'],
			'Current conditions': {
				'Temperature': current['current']['temp_c'],
				'Rain (mm)': current['current']['precip_mm'],
				'Wind (km/h)': current['current']['wind_kph'],
				'Wind direction': current['current']['wind_dir'],
				'Humidity': current['current']['humidity'],
				'UV index': current['current']['uv']
			},
			'Current conditions last updated': current['current']['last_updated'],
			'Daily forecasts': daily_forecasts,
			'Hourly forecasts': hourly_forecasts
		}
		return data
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

#Example-url: localhost:8000/weather/Bologna?Location=Bologna
@router.get("/current/{city}")
async def get_current_weather(city: str):
	try:
		data = weather_service.get_current_weather(city)
		return {
			'Location': city, 
			'Local time': data['location']['localtime'],
			'Current conditions': {
				'Temperature': data['current']['temp_c'],
				'Rain (mm)': data['current']['precip_mm'],
				'Wind (km/h)': data['current']['wind_kph'],
				'Wind direction': data['current']['wind_dir'],
				'Humidity': data['current']['humidity'],
				'UV index': data['current']['uv']
			},
			'Current conditions last updated': data['current']['last_updated']
		}
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

#Example-url: localhost:8000/forecast/daily/Bologna?end_date=2024-11-16
@router.get("/forecast/daily/{city}")
async def get_weather_forecast_daily(city: str, end_date: date):
	try:
		data = weather_service.get_forecast_daily(city, end_date)
		forecasts = make_daily_forecasts(data)
		return {'Location' : city, 'Daily forecasts': forecasts}	
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))
	
def make_daily_forecasts(data):
	forecasts = {}
	for forecast in data:
		date = str(forecast['date'])
		forecasts[date] = {
			'Temperature (avg)': forecast['day']['avgtemp_c'],
			'Rain (mm)': forecast['day']['totalprecip_mm'],
			'Wind (km/h)': forecast['day']['maxwind_kph'],
			'Humidity': forecast['day']['avghumidity'],
			'UV index': forecast['day']['uv']
		}
	return forecasts
	

#Example-url: localhost:8000/forecast/hourly/Bologna?end_datetime=2024-11-17T00:00:00
@router.get("/forecast/hourly/{city}")
async def get_weather_forecast_hourly(city: str, end_datetime: datetime):
	try:
		data = weather_service.get_forecast_hourly(city, end_datetime)
		forecasts = make_hourly_forecasts(data)
		return {"Location": city, "Hourly forecasts": forecasts}	
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))
	
def make_hourly_forecasts(data):
	forecasts = {}
	for forecast in data:
		time = str(forecast['time'])
		forecasts[time] = {
			'Temperature': forecast['temp_c'],
			'Rain (mm)': forecast['precip_mm'],
			'Wind (km/h)': forecast['wind_kph'],
			'Humidity': forecast['humidity'],
			'UV index': forecast['uv']
		}
	return forecasts