import asyncio
from aiogram import Bot, Dispatcher

from telegram_bot.handlers import router

def run_telegram_bot(token_bot, sats_coors, step, lons_obs, lats_obs, tles, passes, 
                     obs_lon, obs_lat, obs_alt, end_time_hours):
    async def main():
        bot  = Bot(token = token_bot)
        dp = Dispatcher()

        dp["sats_coors"] = sats_coors
        dp["step"] = step
        dp["obs_lon"] = lons_obs
        dp["obs_lat"] = lats_obs
        dp["sats_tle"] = tles
        dp["passes"] = passes
        dp["obs_lon"] = obs_lon
        dp["obs_lat"] = obs_lat
        dp["obs_alt"] = obs_alt
        dp["end_time_hours"] = end_time_hours

        dp.include_router(router)
        await dp.start_polling(bot)

    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print('Бот остановлен ')
