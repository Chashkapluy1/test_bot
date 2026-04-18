from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    welcome_text = (
        "Hello! I am your Smart Weather & Travel AI Assistant 🌍✈️\n\n"
        "Tell me where you are or where you plan to go, and I'll not only tell you the weather "
        "but also suggest what to wear and what to do! \n\n"
        "Try asking: 'What's the weather like in Paris?'"
    )
    await message.answer(welcome_text)
