from app.config.settings import settings
from datetime import date, datetime
import requests

class WeatherService:
    def __init__(self):
        self.base_url = "http://api.weatherapi.com/v1/"
        self.api_key = settings.WEATHER_API_KEY

    def get_current_weather(self, city: str):
        url = f"{self.base_url}current.json?key={self.api_key}&q={city}&aqi=no"
        response = requests.get(url)
        response.raise_for_status()

        return response.json()
    
    def get_forecast_daily(self, city, end_date: date):
        today = date.today()

        if end_date < today:
            raise ValueError("End date must be today or later")
        
        days = (end_date - today).days + 1

        if days < 0 or days > 10:
            raise ValueError("End date can't be more than 9 days from today")
        
        url = f"{self.base_url}forecast.json?key={self.api_key}&q={city}&days={days}&aqi=no"
        response = requests.get(url)
        response.raise_for_status()
        res = response.json()
        forecast = res['forecast']['forecastday']

        return forecast
    
    def get_forecast_hourly(self, city, end_datetime: datetime):
        today = datetime.now()
        now_epoch_time = int(today.timestamp())
        epoch_end_time = int(end_datetime.timestamp())

        if end_datetime < today:
            raise ValueError("End date must be later than now")
        
        days = (end_datetime.date() - today.date()).days + 1

        if days < 0 or days > 10:
            raise ValueError("End time can't be more than 9 days from now")
        
        url = f"{self.base_url}forecast.json?key={self.api_key}&q={city}&days={days}&aqi=no"
        response = requests.get(url)
        response.raise_for_status()
        res = response.json()
        forecasts = res['forecast']['forecastday']
        forecasts_trimmed = []
        for forecast in forecasts:
            hours = forecast['hour']
            for hour in hours:
                if hour['time_epoch'] >= now_epoch_time and hour['time_epoch'] <= epoch_end_time:
                    forecasts_trimmed.append(hour) 

        return forecasts_trimmed
        