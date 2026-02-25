from aiogram import Router, F
from aiogram.types import Message
from bot.services.ai import ai_service

router = Router()

@router.message(F.text)
async def handle_text_message(message: Message):
    """
    Global text message handler with UX improvements (typing actions).
    """
    if not message.text:
        return

    await message.bot.send_chat_action(chat_id=message.chat.id, action="typing")
    
    reply_text = await ai_service.process_message(
        user_id=message.from_user.id, 
        text=message.text
    )
    
    await message.answer(reply_text)
