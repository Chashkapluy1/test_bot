import logging
import aiohttp
from typing import TypedDict, Optional, Union
from bot.config import config

logger = logging.getLogger(__name__)

class WeatherData(TypedDict):
    city: str
    country: str
    temperature: float
    feels_like: float
    description: str
    wind_speed: float

class WeatherError(TypedDict):
    error: str

class WeatherService:
    """
    Service responsible for fetching weather data from OpenWeatherMap.
    """
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

    def __init__(self, api_key: str):
        self.api_key = api_key

    async def fetch_weather(self, city: str) -> Union[WeatherData, WeatherError]:
        """
        Get current weather data for a given city.
        """
        params = {
            "q": city,
            "appid": self.api_key,
            "units": "metric",
            "lang": "en"
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.BASE_URL, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        return {
                            "city": data['name'],
                            "country": data['sys']['country'],
                            "temperature": data['main']['temp'],
                            "feels_like": data['main']['feels_like'],
                            "description": data['weather'][0]['description'],
                            "wind_speed": data['wind']['speed']
                        }
                    
                    error_msg = f"API returned {response.status}"
                    if response.status == 404:
                        error_msg = f"City '{city}' not found."
                    
                    logger.warning(f"Weather API error: {error_msg}")
                    return {"error": error_msg}
                    
        except aiohttp.ClientError as e:
            logger.exception("Network error while reaching Weather API")
            return {"error": "Connection error to weather service."}
        except Exception:
            logger.exception("Unexpected error in WeatherService")
            return {"error": "Internal weather service error."}

weather_service = WeatherService(config.WEATHER_API_KEY)
