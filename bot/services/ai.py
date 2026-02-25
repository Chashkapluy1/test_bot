import logging
from typing import Dict, Any, List

import google.generativeai as genai
from google.generativeai.types import content_types

from bot.config import config
from bot.services.weather import weather_service

logger = logging.getLogger(__name__)

class AIService:
    """
    Orchestrates interaction with Gemini 1.5/2.5 Flash, 
    managing tool use (Function Calling) flow.
    """
    
    def __init__(self, api_key: str, model_name: str = "gemini-2.5-flash"):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(
            model_name=model_name,
            tools=self._setup_tools(),
            system_instruction=(
                "You are an elite Smart Weather & Travel AI Assistant. "
                "Help users with precise weather forecasts and travel advice. "
                "When a user asks about the weather in a specific location, ALWAYS use 'get_weather'. "
                "Synthesize the raw data into a friendly, professional, yet conversational response. "
                "Provide context-aware tips (clothing, activities)."
            )
        )
        self._user_chats: Dict[int, Any] = {}

    def _setup_tools(self) -> List[Dict[str, Any]]:
        return [{
            "function_declarations": [
                {
                    "name": "get_weather",
                    "description": "Fetch real-time weather information for a specific city.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "city": {"type": "string", "description": "City name (e.g., Berlin, Dubai)"}
                        },
                        "required": ["city"]
                    }
                }
            ]
        }]

    async def process_message(self, user_id: int, text: str) -> str:
        """
        Main entrypoint for processing user text via LLM.
        """
        if user_id not in self._user_chats:
            self._user_chats[user_id] = self.model.start_chat()
        
        chat = self._user_chats[user_id]
        
        try:
            response = await chat.send_message_async(text)
            
            # Handle potential tool calls sequentially
            for part in response.candidates[0].content.parts:
                if part.function_call:
                    return await self._execute_tool_and_reply(chat, part.function_call)
                    
            return response.text
            
        except Exception:
            logger.exception(f"Critical error in AI Service for user {user_id}")
            return "I apologize, but I encountered an internal error. Please try again in a moment."

    async def _execute_tool_and_reply(self, chat: Any, func_call: Any) -> str:
        """
        Executes the requested tool and feeds results back to the model.
        """
        if func_call.name == "get_weather":
            city = func_call.args.get("city")
            logger.info(f"Executing tool 'get_weather' for city: {city}")
            
            weather_data = await weather_service.fetch_weather(city)
            
            # Encapsulate response in proper SDK protos
            tool_response = [
                content_types.protos.Part(
                    function_response=content_types.protos.FunctionResponse(
                        name="get_weather",
                        response={"result": weather_data}
                    )
                )
            ]
            
            final_response = await chat.send_message_async(tool_response)
            return final_response.text
            
        return "Target tool not found."

ai_service = AIService(config.GEMINI_API_KEY)
