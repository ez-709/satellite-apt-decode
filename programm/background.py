from skyfield.api import load, utc
from datetime import datetime
import os
import time
import random
import traceback

from storage import (json_to_py, active_names, create_urls_to_htpp, write_or_update_tles, 
                     update_calculations, write_logs)
from tracking.parsing import get_not_deb_tle
from tracking.calculation import calculate_orbit, calculate_samples_from_hours, calculate_passes
from tracking.utils import find_next_time_for_updating_calculations, unix_to_utc

def background_update_tles(update=False):
    cd = os.getcwd()
    cd_sat = os.path.join(cd, 'programm', 'data', 'data_base', 'satellites.json')
    cd_tle = os.path.join(cd, 'programm', 'data', 'data_base', 'tle.json')
    cd_logs_htpp = os.path.join(cd, 'programm', 'data', 'logs', 'logs_htpp.txt')

    tles = []
    urls = create_urls_to_htpp(cd_sat)

    def process_urls():
        nonlocal tles
        for i, url in enumerate(urls):
            try:
                if i > 0:
                    time.sleep(random.uniform(1, 3))

                new_tles = get_not_deb_tle(url, active_names(cd_sat))
                if new_tles == 429:
                    write_logs(cd_logs_htpp, f'429 - слишком много запросов для {url} в {unix_to_utc(time.time())}')
                    time.sleep(60 * 60)

                elif new_tles == 403:
                    write_logs(cd_logs_htpp, f'403 - доступ запрещен для {url} в {unix_to_utc(time.time())}')
                    break

                elif isinstance(new_tles, int) and new_tles >= 400:
                    write_logs(cd_logs_htpp, f'HTTP ошибка {new_tles} для {url} в {unix_to_utc(time.time())}')
                    continue

                elif new_tles:
                    tles.append(new_tles)
                    write_logs(cd_logs_htpp, f"Успешно получено {len(new_tles)} TLE из {url} в {unix_to_utc(time.time())}")

            except Exception as e:
                write_logs(cd_logs_htpp, f"Неожиданная ошибка для {url}: {e} в {unix_to_utc(time.time())}")
                time.sleep(600)
                continue

        if tles:
            for tle_group in tles:
                write_or_update_tles(tle_group, cd_tle)
            write_logs(cd_logs_htpp, f"Обновлено TLE для {sum(len(t) for t in tles)} спутников в {unix_to_utc(time.time())}")


    if update == True:
        process_urls()
    else:
        while True:
            process_urls()
            sleep_time = 60 * 60 * random.uniform(24, 48)
            write_logs(cd_logs_htpp, f"Следующий htpp запрос будет в {unix_to_utc(time.time() + sleep_time)}")
            time.sleep(sleep_time)
            

def make_all_calculations(obs_lon, obs_lat, obs_alt, end_time_hours):
    cd = os.getcwd() 
    cd_tle = os.path.join(cd, 'programm', 'data', 'data_base', 'tle.json')
    cd_coordinates = os.path.join(cd, 'programm', 'data', 'data_base', 'coordinates.json')
    cd_passes = os.path.join(cd, 'programm', 'data', 'data_base', 'passes.json')
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
        calc_passes.append(calculate_passes(sat_tle, end_time_hours, obs_lon, obs_lat, obs_alt))

    update_calculations(calc_passes, cd_passes)
    
    return last_time_unix_of_calculations

def background_calculations(obs_lon, obs_lat, obs_alt, end_time_hours):
    cd = os.getcwd() 
    cd_passes = os.path.join(cd, 'programm', 'data', 'data_base', 'passes.json')
    cd_logs_calc = os.path.join(cd, 'programm', 'data','logs', 'logs_tech.txt')
    cd_logs_back = os.path.join(cd, 'programm', 'data','logs', 'logs_back.txt')
    passes = json_to_py(cd_passes)
    next_time = time.time()   
    while True:
        try:
            time_now = time.time()
            
            if time_now >= next_time:
                time_start = time.time()
                last_time_unix = make_all_calculations(obs_lon, obs_lat, obs_alt, end_time_hours)
                next_time = find_next_time_for_updating_calculations(last_time_unix, passes)
                last_time_utc = unix_to_utc(last_time_unix)
                next_time_utc = unix_to_utc(next_time)
                text = f'В последний раз вычисления обновлялись в {last_time_utc}\n'
                text += f'Следующее обновление вычислений будет в {next_time_utc}'
                write_logs(cd_logs_calc, text, update=False)
                time_end = time.time()
                write_logs(cd_logs_back, f'вычисления заняли {round(time_start-time_end)} секунд \n')
                print('Вычисления обновлены')

            time.sleep(30)     
        except Exception as e:
            error_info = traceback.format_exc()
            text = f"Ошибка в background: {e}\nДетали:\n{error_info}\n\n"
            text += f' в {unix_to_utc(time.time())}\n\n'
            write_logs(cd_logs_back, text)
            time.sleep(60)
