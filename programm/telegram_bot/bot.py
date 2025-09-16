import asyncio
from aiogram import Bot, Dispatcher
import time

from telegram_bot.handlers import router
from storage import json_to_py

def run_telegram_bot(token, obs_lon, obs_lat, obs_alt, step, end_time_hours):
    
    async def main():
        bot = Bot(token=token)
        dp = Dispatcher()
        
        dp["obs_lon"] = obs_lon
        dp["obs_lat"] = obs_lat
        dp["obs_alt"] = obs_alt
        dp["step"] = step
        dp["end_time_hours"] = end_time_hours

        dp.include_router(router)

        try:
            await dp.start_polling(bot)
        finally:
            pass
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print('Бот остановлен')