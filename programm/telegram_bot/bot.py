import asyncio
from aiogram import Bot, Dispatcher
import time

from telegram_bot.handlers import router
from storage import json_to_py

def run_telegram_bot(token, obs_lon, obs_lat, obs_alt, step, end_time_hours, 
                     cd_tles, cd_coors, cd_passes):
    
    async def update_data_periodically(dp):
        while True:
            try:
                tles = json_to_py(cd_tles)
                sats_coors = json_to_py(cd_coors) 
                passes = json_to_py(cd_passes)
                
                dp["sats_tle"] = tles
                dp["sats_coors"] = sats_coors
                dp["passes"] = passes
                
                await time.sleep(24 * 60 * 60) 
            except Exception as e:
                print(f"Ошибк* при обновлении данных: {e}")
                await time.sleep(60) 

    async def main():
        bot = Bot(token=token)
        dp = Dispatcher()
        
        dp["obs_lon"] = obs_lon
        dp["obs_lat"] = obs_lat
        dp["obs_alt"] = obs_alt
        dp["step"] = step
        dp["end_time_hours"] = end_time_hours

        dp["sats_tle"] = json_to_py(cd_tles)
        dp["sats_coors"] = json_to_py(cd_coors)
        dp["passes"] = json_to_py(cd_passes)
        
        dp.include_router(router)

        update_task = asyncio.create_task(update_data_periodically(dp))
        
        try:
            await dp.start_polling(bot)
        finally:
            update_task.cancel()
            try:
                await update_task
            except asyncio.CancelledError:
                pass

    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print('Бот остановлен')