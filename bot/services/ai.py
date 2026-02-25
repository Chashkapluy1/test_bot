import google.generativeai as genai
from google.generativeai.types import content_types
from bot.config import config
from bot.services.weather import get_weather
import logging

logger = logging.getLogger(__name__)

genai.configure(api_key=config.GEMINI_API_KEY)

weather_tool = {
    "function_declarations": [
        {
            "name": "get_weather",
            "description": "Get current weather data for a given city.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "The name of the city, e.g. London, Tokyo or Moscow"
                    }
                },
                "required": ["city"]
            }
        }
    ]
}

model = genai.GenerativeModel(
    model_name='gemini-2.5-flash',
    tools=weather_tool,
    system_instruction=(
        "You are a Smart Weather & Travel AI Assistant. "
        "Your primary goal is to help users with weather forecasts and give advice on what to wear or where to go based on the current weather. "
        "Always use the get_weather tool when the user mentions a city or explicitly asks for the weather. "
        "After receiving the weather data, explain it to the user in a helpful, friendly, and conversational way. "
        "Suggest clothing or activities appropriate for the temperature and weather conditions."
    )
)

user_chats = {}

async def get_ai_response(user_id: int, message: str) -> str:
    """
    Process user message via Gemini AI, invoking the weather function if needed.
    """
    if user_id not in user_chats:
        user_chats[user_id] = model.start_chat()
    
    chat = user_chats[user_id]
    
    try:
        # Send user message to Gemini
        response = await chat.send_message_async(message)
        
        # Check if Gemini decided to call a function
        if response.candidates and response.candidates[0].content.parts:
            for part in response.candidates[0].content.parts:
                if part.function_call:
                    func_call = part.function_call
                    if func_call.name == "get_weather":
                        city = type(func_call).to_dict(func_call).get('args', {}).get("city")
                        if not city:
                            # Fallback if arg parsing differs
                            city = getattr(func_call.args, 'city', None) or dict(func_call.args).get("city")

                        logger.info(f"AI requested weather for city: {city}")
                        
                        if city:
                            # 1. Call the external API
                            weather_data = await get_weather(city)
                            logger.info(f"Weather data retrieved: {weather_data}")
                            
                            # 2. Return data back to Gemini
                            function_response = [
                                content_types.Part.from_function_response(
                                    name="get_weather",
                                    response={"result": weather_data}
                                )
                            ]
                            response = await chat.send_message_async(function_response)
        
        return response.text
    except Exception as e:
        logger.error(f"Error in AI service: {e}")
        return "Sorry, I encountered an error while processing your request. Please try again later."
