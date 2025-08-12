from skyfield.api import load
import os
import threading

from storage import json_to_py, find_satellites, read_config
from tracking.calculation import calculate_samples_from_hours
from tracking.visualization import visualization_orbit_for_satellites
from tracking.utils import filter_by_names, check_end_time_hours_correct
from background import background
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

obs_lon, obs_lat,  obs_alt, end_time_hours, token = read_config(cd_config)
samples, step  = calculate_samples_from_hours(end_time_hours)
sats_tle = json_to_py(cd_tle)
sats_coor = json_to_py(cd_coordinates)

'''
background_thread = threading.Thread(
    target=background, 
    args=(obs_lon, obs_lat, obs_alt, end_time_hours),
    daemon=True
)
background_thread.start()
'''
'''
if check_end_time_hours_correct(unix_time_now, 3, sats_coor) == True:
    sat_inf = json_to_py(cd_coordinates)
    names, filter_of = find_satellites(cd_sat)
    sat_inf = filter_by_names(names, sat_inf)
    visualization_orbit_for_satellites(sat_inf, unix_time_now, 3, step, obs_lon, obs_lat, names, filter_of)
'''

run_telegram_bot(token)