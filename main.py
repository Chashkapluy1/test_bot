import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from bot.config import config
from bot.handlers import commands, messages

# Setup logger configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    stream=sys.stdout,
)
logger = logging.getLogger(__name__)

import os
from aiohttp import web

async def health_check(request):
    return web.Response(text="Bot is running!")

async def start_health_server():
    app = web.Application()
    app.router.add_get("/", health_check)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    logger.info(f"Health check server started on port {port}")

async def main():
    logger.info("Starting bot...")
    
    # Start health check server for Render
    await start_health_server()
    
    # Initialize bot and dispatcher
    bot = Bot(token=config.BOT_TOKEN)
    dp = Dispatcher()
    
    # Include routers
    dp.include_router(commands.router)
    dp.include_router(messages.router)
    
    try:
        # Avoid processing old updates
        await bot.delete_webhook(drop_pending_updates=True)
        # Start polling
        await dp.start_polling(bot)
    finally:
        logger.info("Graceful shutdown started.")
        await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped.")
