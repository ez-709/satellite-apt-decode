import os
import time

from decode.rtl_sdr import record_radio_wav
from decode.decoder_apt import decoder_apt
from storage import json_to_py, make_decode_results_names, folder_name_by_sat_name, write_new_passes

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
            frequency = sat["frequency"] * 1e3
            frequency = 90.2e3

    record_radio_wav(frequency, cd_record_wav, duration, gain, bandwidth)

    decoder_apt(cd_record_wav, cd_record_img)

    write_new_passes(cd_sat_record, cd_record_wav, cd_record_img, name_of_satellite)
    print(name_of_satellite)

def recors_sats_from_passes():
    cd = os.getcwd()
    cd_passes = os.path.join(cd, 'programm', 'data', 'data_base', 'passes.json')
    passes = json_to_py(cd_passes)
    sorted_passes = []
    for satellite in passes:
        name = satellite['name']
        for point in satellite['points']:
            sorted_passes.append({
                'name': name,
                'rise': point['rise'],
                'duration': point['duration (min:sec)']
            })
    sorted_passes.sort(key=lambda x: x.split('в ')[1].split('\n')[0])
    return passes