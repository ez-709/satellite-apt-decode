from skyfield.api import load
import os

from storage import json_to_py, find_satellites, read_config
from tracking.utils import check_end_time_hours_correct
from tracking.calculation import calculate_samples_from_hours
from tracking.visualization import visualization_orbit_for_satellites
from tracking.utils import filter
from background import background

ts = load.timescale()
unix_time_now = ts.now().utc_datetime().timestamp()

cd = os.getcwd() 
cd_sat = os.path.join(cd, 'programm', 'data', 'data_base', 'satellites.json')
cd_tle = os.path.join(cd, 'programm', 'data', 'data_base', 'tle.json')
cd_processing = os.path.join(cd, 'programm', 'data', 'data_base', 'processing.json')
cd_coordinates = os.path.join(cd, 'programm', 'data', 'data_base', 'coordinates.json')
cd_passes = os.path.join(cd, 'programm', 'data', 'data_base', 'passes.json')
cd_config = os.path.join(cd, 'programm', 'config.json')

obs_lon, obs_lat,  obs_alt, end_time_hours = read_config(cd_config)
samples, step  = calculate_samples_from_hours(end_time_hours)
sats_tle = json_to_py(cd_tle)
sats_coor = json_to_py(cd_coordinates)

#last_time_utc_of_calculations = background(obs_lon, obs_lat,  obs_alt, end_time_hours)

if check_end_time_hours_correct(unix_time_now, 3, sats_coor) == True:
    sat_inf = json_to_py(cd_coordinates)
    names, filter_of = find_satellites(cd_sat)
    sat_inf = filter(names, sat_inf)
    visualization_orbit_for_satellites(sat_inf, unix_time_now, 3, step, obs_lon, obs_lat, obs_alt, names, filter_of)

#ПРОВЕРИТЬ ВЕЗДЕ ЛИ РАБОТАЕТ ФИЛЬТР
#дописать условие, что если один спутник на взод визуализации, то поменять заголовок
#добавить условие на наличие пролета в данный момент, и добавить приоритет по пролетам,
#если их два одновременно

