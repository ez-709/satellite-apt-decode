import asyncio
from aiogram import Bot, Dispatcher
import time

from telegram_bot.handlers import router

def run_telegram_bot(
    token, obs_lon, obs_lat, obs_alt, step, end_time_hours,
    cd_sat, cd_tle, cd_coordinates, cd_passes, cd_config, cd_decode,
    cd_logs_htpp, cd_logs_tech, cd_logs_back, cd_logs_decode
):
    async def main():
        bot = Bot(token=token)
        dp = Dispatcher()

        dp["obs_lon"] = obs_lon
        dp["obs_lat"] = obs_lat
        dp["obs_alt"] = obs_alt
        dp["step"] = step
        dp["end_time_hours"] = end_time_hours

        dp["cd_sat"] = cd_sat
        dp["cd_tle"] = cd_tle
        dp["cd_coordinates"] = cd_coordinates
        dp["cd_passes"] = cd_passes
        dp["cd_config"] = cd_config
        dp["cd_decode"] = cd_decode
        dp["cd_logs_htpp"] = cd_logs_htpp
        dp["cd_logs_tech"] = cd_logs_tech
        dp["cd_logs_back"] = cd_logs_back
        dp["cd_logs_decode"] = cd_logs_decode

        dp.include_router(router)

        try:
            await dp.start_polling(bot)
        finally:
            await bot.session.close()

    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print('Бот остановлен')