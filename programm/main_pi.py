import os
import threading
import time
import traceback

from common.storage import (json_to_py, read_config, add_rtl_sdr_libs_to_venv, 
                     clear_all_logs, create_decode_folders_by_names)

cd = os.getcwd() 
cd_config = os.path.join(cd, 'programm', 'config.json')
cd_sat = os.path.join(cd, 'programm', 'pi', 'data', 'data_base', 'satellites.json')
cd_sat_record = os.path.join(cd, 'programm','pi', 'data', 'data_base', 'sat_records.json')
cd_passes = os.path.join(cd, 'programm','pi', 'data', 'passes.json')
cd_recorde = os.path.join(cd, 'programm','pi', 'data_decode')
cd_logs_pi = os.path.join(cd, 'programm','pi', 'data', 'logs_pi.txt')
cd_logs_decode_pi = os.path.join(cd, 'programm','pi', 'data', 'logs_decode_pi.txt')

cd_libs = os.path.join(cd, 'programm','pi', 'data', 'rlt_sdr_libs')

#clear_all_logs(cd_logs_pi = cd_logs_pi, pi_mode = True)

obs_lon, obs_lat, obs_alt, time_zone, step, end_time_hours, token, venv_name = read_config(cd_config)
cd_venv = os.path.join(cd, venv_name)

add_rtl_sdr_libs_to_venv(cd, cd_venv, cd_libs) #будет ошибка, если файлы dll для rtl_sdr не былм доавлены в venv/Scripts предварительно

from pi.recording_procesing import recors_sats_from_passes

background_recorder = threading.Thread(
    target=recors_sats_from_passes, 
    args=(cd_passes, cd_logs_pi, cd_logs_decode_pi, cd_recorde, cd_sat, cd_sat_record),
    daemon=True
)
background_recorder.start()
print('sosal')
time.sleep(2000000)