from skyfield.api import load
import os

from common.storage import (json_to_py, read_config, add_rtl_sdr_libs_to_venv, 
                     clear_all_logs, create_decode_folders_by_names)

ts = load.timescale()
unix_time_now = ts.now().utc_datetime().timestamp()

cd = os.getcwd() 
cd_config = os.path.join(cd, 'programm', 'config.json')
cd_sat_record = os.path.join(cd, 'programm','pi', 'data', 'data_base', 'sat_records.json')
cd_decode = os.path.join(cd, 'programm','pi', 'data_decode')
cd_logs_pi = os.path.join(cd, 'programm','pi', 'data', 'logs_pi.txt')

cd_libs = os.path.join(cd, 'programm','pi', 'decode', 'rlt_sdr_libs')

clear_all_logs(cd_logs_pi = cd_logs_pi, pi_mode = True)

obs_lon, obs_lat, obs_alt, time_zone, step, end_time_hours, token, venv_name = read_config(cd_config)
cd_venv = os.path.join(cd, venv_name)

add_rtl_sdr_libs_to_venv(cd, cd_venv, cd_libs) #будет ошибка, если файлы dll для rtl_sdr не былм доавлены в venv/Scripts предварительно

#from pi.decoding_procesing import recors_sats_from_passes
