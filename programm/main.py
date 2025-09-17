from skyfield.api import load
import os
import threading
import time
import traceback

from storage import (json_to_py, read_config, add_rtl_sdr_libs_to_venv, 
                     clear_all_logs, create_decode_folders_by_names, create_sat_record_sructure)
from tracking.calculation import calculate_samples_from_hours
from background import background_calculations, background_update_tles
from telegram_bot.bot import run_telegram_bot

ts = load.timescale()
unix_time_now = ts.now().utc_datetime().timestamp()

cd = os.getcwd() 
cd_sat = os.path.join(cd, 'programm', 'data', 'data_base', 'satellites.json')
cd_config = os.path.join(cd, 'programm', 'config.json')

cd_tle = os.path.join(cd, 'programm', 'data', 'data_base', 'tle.json')
cd_coordinates = os.path.join(cd, 'programm', 'data', 'data_base', 'coordinates.json')
cd_passes = os.path.join(cd, 'programm', 'data', 'data_base', 'passes.json')
cd_sat_record = os.path.join(cd, 'programm', 'data', 'data_base', 'sat_records.json')

cd_decode = os.path.join(cd, 'programm', 'data_decode')
cd_logs_htpp = os.path.join(cd, 'programm', 'data','logs', 'logs_htpp.txt')
cd_logs_tech = os.path.join(cd, 'programm', 'data','logs', 'logs_tech.txt')
cd_logs_back = os.path.join(cd, 'programm', 'data','logs', 'logs_back.txt')

sats = json_to_py(cd_sat)
names = [sat['name'] for sat in sats]

create_sat_record_sructure(cd_sat_record, names)

create_decode_folders_by_names(cd_decode, names)

clear_all_logs(cd_logs_back, cd_logs_htpp, cd_logs_tech)

obs_lon, obs_lat, obs_alt, time_zone, step, end_time_hours, token, venv_name = read_config(cd_config)
cd_venv = os.path.join(cd, venv_name)
add_rtl_sdr_libs_to_venv(cd, cd_venv)
samples, step = calculate_samples_from_hours(end_time_hours)
tles = json_to_py(cd_tle)
sats_coor = json_to_py(cd_coordinates)
passes = json_to_py(cd_passes)

calculation_complete_event = None

try:
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

    while True:
        try:
            run_telegram_bot(token, obs_lon, obs_lat, obs_alt, step, end_time_hours)
        except Exception as e:
            error_time = time.asctime(time.localtime(time.time()))
            tb = traceback.extract_tb(e.__traceback__)[-1]
            file_name = tb.filename.split('\\')[-1]
            line_number = tb.lineno96
            error_message = f'{error_time} - Ошибка в работе бота ({file_name}, строка {line_number}): {str(e)}\n'
            
            try:
                with open(cd_logs_back, 'a', encoding='utf-8') as f:
                    f.write(error_message)
            except:
                pass
            
            time.sleep(10)
            continue

except Exception as e:
    error_time = time.asctime(time.localtime(time.time()))
    tb = traceback.extract_tb(e.__traceback__)[-1]
    file_name = tb.filename.split('\\')[-1]
    line_number = tb.lineno
    error_message = f'{error_time} - Ошибка в ({file_name}, строка {line_number}): {str(e)}\n'
    
    try:
        with open(cd_logs_back, 'a', encoding='utf-8') as f:
            f.write(error_message)
    except:
        pass
    