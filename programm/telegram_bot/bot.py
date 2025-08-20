import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram.filters import Command, CommandStart

from telegram_bot.handlers import router

def run_telegram_bot(token_bot, sats_coors, step, lons_obs, lats_obs, tles, passes):
    async def main():
        bot  = Bot(token = token_bot)
        dp = Dispatcher()

        dp["sats_coors"] = sats_coors
        dp["step"] = step
        dp["obs_lon"] = lons_obs
        dp["obs_lat"] = lats_obs
        dp["sats_tle"] = tles
        dp["passes"] = passes

        dp.include_router(router)
        await dp.start_polling(bot)

    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print('Бот остановлен ')
