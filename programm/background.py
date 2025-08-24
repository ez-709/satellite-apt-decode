from skyfield.api import load, utc
from datetime import datetime
import os
import time
import traceback

from storage import json_to_py, active_names, create_urls_to_htpp
from storage import write_or_update_tles, update_calculations
from tracking.parsing import get_not_deb_tle
from tracking.calculation import calculate_orbit, calculate_samples_from_hours, calculate_passes
from tracking.utils import find_next_time_for_updating_calculations

def make_all_calculations(obs_lon, obs_lat, obs_alt, end_time_hours):
    cd = os.getcwd() 
    cd_sat = os.path.join(cd, 'programm', 'data', 'data_base', 'satellites.json')
    cd_tle = os.path.join(cd, 'programm', 'data', 'data_base', 'tle.json')
    cd_coordinates = os.path.join(cd, 'programm', 'data', 'data_base', 'coordinates.json')
    cd_passes = os.path.join(cd, 'programm', 'data', 'data_base', 'passes.json')
    dt = datetime.now(tz=utc)
    last_time_unix_of_calculations = dt.timestamp()

    samples, step  = calculate_samples_from_hours(end_time_hours)
    
    
    tles = []
    urls = create_urls_to_htpp(cd_sat)
    for url in urls:
        new_tles = get_not_deb_tle(url, active_names(cd_sat))
        tles.append(new_tles)
    for tle_group in tles:
        write_or_update_tles(tle_group, cd_tle)
    calc_sats = []
    sats_tle = json_to_py(cd_tle)
    for sat_tle in sats_tle:
        calc_sats.append(calculate_orbit(sat_tle, end_time_hours, samples))

    update_calculations(calc_sats, cd_coordinates)
    calc_passes = []
    for sat_tle in sats_tle:
        calc_passes.append(calculate_passes(sat_tle, end_time_hours, obs_lon, obs_lat, obs_alt))

    update_calculations(calc_passes, cd_passes)
    
    return last_time_unix_of_calculations

def background(obs_lon, obs_lat, obs_alt, end_time_hours):
    cd = os.getcwd() 
    cd_passes = os.path.join(cd, 'programm', 'data', 'data_base', 'passes.json')
    passes = json_to_py(cd_passes)
    next_time = time.time()   
    while True:
        try:
            time_now = time.time()
            
            if time_now >= next_time:
                last_time_unix = make_all_calculations(obs_lon, obs_lat, obs_alt, end_time_hours)
                next_time = find_next_time_for_updating_calculations(last_time_unix, passes)
                print(f'Обновлены вычисления в {datetime.fromtimestamp(time_now)}')
                print(f"Следующий расчет: {datetime.fromtimestamp(next_time)}")
                print(f"Разница: {next_time - time_now} секунд")
                print()

            time.sleep(5)     
        except Exception as e:
            error_message = traceback.format_exc()
            print(f"Ошибка в background: {e}")
            print(f"Полный стек вызовов:\n{error_message}")
            time.sleep(60)
