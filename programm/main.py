from skyfield.api import load
import os
import threading
import time

from storage import json_to_py, read_config, add_rtl_sdr_libs_to_venv
from tracking.calculation import calculate_samples_from_hours
from background import background_calculations, background_update_tles
from telegram_bot.bot import run_telegram_bot

ts = load.timescale()
unix_time_now = ts.now().utc_datetime().timestamp()

cd = os.getcwd() 
cd_sat = os.path.join(cd, 'programm', 'data', 'data_base', 'satellites.json')
cd_tle = os.path.join(cd, 'programm', 'data', 'data_base', 'tle.json')
cd_processing = os.path.join(cd, 'programm', 'data', 'data_base', 'processing.json')
cd_coordinates = os.path.join(cd, 'programm', 'data', 'data_base', 'coordinates.json')
cd_passes = os.path.join(cd, 'programm', 'data', 'data_base', 'passes.json')
cd_config = os.path.join(cd, 'programm', 'config.json')
cd_decode = os.path.join(cd, 'programm', 'data_decode')

obs_lon, obs_lat, obs_alt, end_time_hours, token, venv_name = read_config(cd_config)
cd_venv = os.path.join(cd, venv_name)
add_rtl_sdr_libs_to_venv(cd, cd_venv)
samples, step = calculate_samples_from_hours(end_time_hours)
tles = json_to_py(cd_tle)
sats_coor = json_to_py(cd_coordinates)
passes = json_to_py(cd_passes)

background_thread = threading.Thread(
    target=background_calculations, 
    args=(obs_lon, obs_lat, obs_alt, end_time_hours),
    daemon=True
)
background_thread.start()

background_tles_thread = threading.Thread(
    target=background_update_tles, 
    args=(),
    daemon=True
)
background_tles_thread.start()

run_telegram_bot(token, sats_coor, step, obs_lon, obs_lat, tles, passes) 