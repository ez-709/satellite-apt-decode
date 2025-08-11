import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram.filters import Command, CommandStart

from telegram_bot.handlers import router

def run_telegram_bot(token_bot):
    async def main():
        bot  = Bot(token = token_bot)
        dp = Dispatcher()
        dp.include_router(router)
        await dp.start_polling(bot)

    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print('Бот остановлен ')
