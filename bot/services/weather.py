import aiohttp
import logging
from bot.config import config

logger = logging.getLogger(__name__)

async def get_weather(city: str) -> dict:
    """
    Get current weather data for a given city via OpenWeatherMap API.

    Args:
        city: The name of the city.

    Returns:
        A dictionary containing weather information or an error message.
    """
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": config.WEATHER_API_KEY,
        "units": "metric",
        "lang": "en"
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    weather_desc = data['weather'][0]['description']
                    temp = data['main']['temp']
                    feels_like = data['main']['feels_like']
                    wind_speed = data['wind']['speed']
                    return {
                        "city": data['name'],
                        "country": data['sys']['country'],
                        "temperature": temp,
                        "feels_like": feels_like,
                        "description": weather_desc,
                        "wind_speed": wind_speed
                    }
                elif response.status == 404:
                    return {"error": f"City '{city}' not found."}
                elif response.status == 401:
                    return {"error": "Invalid Weather API key."}
                else:
                    return {"error": f"Weather API returned status code {response.status}."}
    except Exception as e:
        logger.error(f"Error fetching weather: {e}")
        return {"error": "Failed to connect to weather service."}
