from skyfield.api import load, utc
from datetime import datetime
import os
import time
import random
import traceback

from tracking.parsing import process_urls
from storage import json_to_py, update_calculations, write_logs
from tracking.calculation import calculate_orbit, calculate_samples_from_hours, calculate_passes
from tracking.utils import find_next_time_for_updating_calculations, unix_to_utc


def background_update_tles(cd_sat, cd_tle, cd_logs_htpp, update=False):
    if update == True:
        process_urls(cd_sat, cd_tle, cd_logs_htpp)
    else:
        while True:
            process_urls(cd_sat, cd_tle, cd_logs_htpp)
            sleep_time = 60 * 60 * random.uniform(24, 48)
            write_logs(cd_logs_htpp, f"Следующий htpp запрос будет в {unix_to_utc(time.time() + sleep_time)}\n\n")
            time.sleep(sleep_time)
            

def make_all_calculations(obs_lon, obs_lat, obs_alt, end_time_hours, cd_sat, cd_tle, cd_coordinates, cd_passes):
    dt = datetime.now(tz=utc)
    last_time_unix_of_calculations = dt.timestamp()

    samples, step  = calculate_samples_from_hours(end_time_hours)

    calc_sats = []
    sats_tle = json_to_py(cd_tle)
    for sat_tle in sats_tle:
        calc_sats.append(calculate_orbit(sat_tle, end_time_hours, samples))

    update_calculations(calc_sats, cd_coordinates)
    calc_passes = []
    for sat_tle in sats_tle:
        calc_passes.append(calculate_passes(cd_sat, sat_tle, end_time_hours, obs_lon, obs_lat, obs_alt))

    update_calculations(calc_passes, cd_passes)
    
    return last_time_unix_of_calculations

def background_calculations(obs_lon, obs_lat, obs_alt, end_time_hours, cd_sat, cd_tle, cd_coordinates, cd_passes, cd_logs_calc, cd_logs_back):
    passes = json_to_py(cd_passes)
    next_time = time.time()   
    while True:
        time_now = time.time()
        try:
            if time_now >= next_time:
                time_start = time.time()
                last_time_unix = make_all_calculations(obs_lon, obs_lat, obs_alt, end_time_hours,cd_sat,  cd_tle, cd_coordinates, cd_passes)
                next_time = find_next_time_for_updating_calculations(last_time_unix, passes, cd_logs_back)
                last_time_utc = unix_to_utc(last_time_unix)
                next_time_utc = unix_to_utc(next_time)
                text = str(next_time) + '\n'
                text += f'В последний раз вычисления обновлялись в {last_time_utc}\n'
                text += f'Следующее обновление вычислений будет в {next_time_utc}\n'
                write_logs(cd_logs_calc, text, update=False)
                time_end = time.time()
                write_logs(cd_logs_back, f'вычисления заняли {round(time_end-time_start)} секунд \n')
                print('Вычисления обновлены')
  
        except Exception as e:
            error_info = traceback.format_exc()
            text = f"Ошибка в background: {e}\nДетали:\n{error_info}\n\n"
            text += f' в {unix_to_utc(time.time())}\n\n'
            write_logs(cd_logs_back, text)
            time.sleep(600)
        time.sleep(30)

def make_all_calculations_ones(obs_lon, obs_lat, obs_alt, end_time_hours, cd_tle, cd_coordinates, cd_passes, cd_logs_calc, cd_logs_back):
    passes = json_to_py(cd_passes)
    next_time = time.time()   
    try:
        time_start = time.time()
        last_time_unix = make_all_calculations(obs_lon, obs_lat, obs_alt, end_time_hours, cd_tle, cd_coordinates, cd_passes)
        next_time = find_next_time_for_updating_calculations(last_time_unix, passes, cd_logs_back)
        last_time_utc = unix_to_utc(last_time_unix)
        next_time_utc = unix_to_utc(next_time)
        text = str(next_time) + '\n'
        text += f'В последний раз вычисления обновлялись в {last_time_utc}\n'
        text += f'Следующее обновление вычислений будет в {next_time_utc}\n'
        write_logs(cd_logs_calc, text, update=False)
        time_end = time.time()
        write_logs(cd_logs_back, f'вычисления заняли {round(time_end - time_start)} секунд \n')
        print('Вычисления обновлены')
  
    except Exception as e:
        error_info = traceback.format_exc()
        text = f"Ошибка в background: {e}\nДетали:\n{error_info}\n\n"
        text += f' в {unix_to_utc(time.time())}\n\n'
        write_logs(cd_logs_back, text)
