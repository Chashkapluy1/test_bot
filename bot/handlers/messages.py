from aiogram import Router, F
from aiogram.types import Message
from bot.services.ai import get_ai_response

router = Router()

@router.message(F.text)
async def handle_text_message(message: Message):
    # Indicate to the user that we are typing/thinking
    await message.bot.send_chat_action(chat_id=message.chat.id, action="typing")
    
    # Process the message through the AI agent
    ai_reply = await get_ai_response(message.from_user.id, message.text)
    
    # Send the final response
    await message.answer(ai_reply)
