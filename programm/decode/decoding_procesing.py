import os
import time

from decode.rtl_sdr import record_radio_wav
from decode.decoder_apt import decoder_apt
from storage import json_to_py, make_decode_results_names, folder_name_by_sat_name, write_new_passes, write_logs
from tracking.utils import sort_passes, unix_to_utc

def record_and_decode_satellite(name_of_satellite, duration, gain = 'auto', bandwidth=2.048e6):
    cd = os.getcwd() 
    cd_decode = os.path.join(cd, 'programm', 'data_decode')
    cd_sats = os.path.join(cd, 'programm', 'data', 'data_base', 'satellites.json')
    cd_sat_record = os.path.join(cd, 'programm', 'data', 'data_base', 'sat_records.json')

    name_folder = folder_name_by_sat_name(name_of_satellite)

    wav_name, img_name = make_decode_results_names(name_of_satellite, time.time())

    cd_record_wav = os.path.join(cd_decode, name_folder, 'wav', wav_name)
    cd_record_img = os.path.join(cd_decode, name_folder, 'img', img_name)
    sats = json_to_py(cd_sats)
    for sat in sats:
        if sat["name"] == name_of_satellite:
            frequency = sat["frequency"] * 1e6
            if frequency > 139 * 1e3:
                frequency = 137 * 1e3

    record_radio_wav(frequency, cd_record_wav, duration, gain, bandwidth)

    #decoder_apt(cd_record_wav, cd_record_img)

    write_new_passes(cd_sat_record, cd_record_wav, cd_record_img, name_of_satellite)

def recors_sats_from_passes():
    cd = os.getcwd()
    cd_passes = os.path.join(cd, 'programm', 'data', 'data_base', 'passes.json')
    cd_logs_tech = os.path.join(cd, 'programm', 'data','logs', 'logs_tech.txt')
    cd_logs_back = os.path.join(cd, 'programm', 'data','logs', 'logs_back.txt')

    passes = json_to_py(cd_passes)
    sorted_passes = sort_passes(passes)
    
    with open(cd_logs_tech, 'r', encoding='utf-8') as file:
        next_time_to_update_passes = float(file.readline().strip())
    
    while True:
        time_now = time.time()
        
        if time_now >= next_time_to_update_passes + 130:
            sorted_passes = sort_passes(passes)
            with open(cd_logs_tech, 'r', encoding='utf-8') as file:
                first_line = file.readline().strip()
                next_time_to_update_passes = float(first_line)

        elif time_now >= sorted_passes[0]['rise'] - 3:
            sat = sorted_passes[0]
            min, sec = sat['duration'].split(':')
            duration = int(min) * 60 + int(sec)
            record_and_decode_satellite(sat['name'], (duration + 60)/60)
            write_logs(cd_logs_back, f'\nЗаписан {sat["name"]} в {unix_to_utc(time.time())}\n')
            sorted_passes.pop(0)
        
        time.sleep(1)