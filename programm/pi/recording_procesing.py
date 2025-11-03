import os
import time

from pi.rtl_sdr import record_radio_wav
from common.storage import json_to_py, make_decode_results_names, folder_name_by_sat_name, write_new_passes, write_logs
from common.utils import sort_passes, unix_to_utc

def record_satellite(name_of_satellite, duration, cd_recorde, cd_sats, cd_sat_record, gain = 'auto', bandwidth=2.048e6):
    name_folder = folder_name_by_sat_name(name_of_satellite)

    wav_name, img_name = make_decode_results_names(name_of_satellite, time.time())

    cd_record_wav = os.path.join(cd_recorde, name_folder, 'wav', wav_name)
    sats = json_to_py(cd_sats)
    for sat in sats:
        if sat["name"] == name_of_satellite:
            frequency = sat["frequency"] * 1e6
            if frequency > 139 * 1e6:
                frequency = 137 * 1e6

    record_radio_wav(frequency, cd_record_wav, duration, gain, bandwidth)

    write_new_passes(cd_sat_record, cd_record_wav, name_of_satellite)

def recors_sats_from_passes(cd_passes, cd_logs_pi, cd_logs_decode, cd_recorde, cd_sats, cd_sat_record):
    passes = json_to_py(cd_passes)
    sorted_passes = sort_passes(passes)

    next_time_to_update_passes = None
    while next_time_to_update_passes is None:
        try:
            with open(cd_logs_pi, 'r', encoding='utf-8') as file:
                line = file.readline().strip()
                if line:
                    next_time_to_update_passes = float(line)
                else:
                    time.sleep(5)  
        except (FileNotFoundError, ValueError, OSError):
            time.sleep(5)
    
    while True:
        try:
            time_now = time.time()
            if time_now >= next_time_to_update_passes + 130:
                passes = json_to_py(cd_passes)
                sorted_passes = sort_passes(passes)
                with open(cd_logs_pi, 'r', encoding='utf-8') as file:
                    first_line = file.readline().strip()
                    next_time_to_update_passes = float(first_line)

            elif time_now >= sorted_passes[0]['rise'] - 3:
                sat = sorted_passes[0]
                min, sec = sat['duration'].split(':')
                duration = int(min) * 60 + int(sec)
                record_satellite(sat['name'], duration + 60,  cd_recorde, cd_sats, cd_sat_record)
                write_logs(cd_logs_decode, f'\nЗаписан {sat["name"]} в {unix_to_utc(time.time())}\n')
                sorted_passes.pop(0)
            
            time.sleep(5)
        except Exception as e:
            write_logs(cd_logs_decode, f"\nОшибка в recors_sats_from_passes: {e}\n")
            time.sleep(10)