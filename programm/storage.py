import json
import numpy as np
import os
import shutil

from tracking.utils import unix_to_utc

def json_to_py(cd_json):
    '''Читает json с путем  'cd_json' и возвращает список словарей'''
    with open(cd_json, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def find_satellites(cd_sat, name=None, norad_id=None, frequency=None, min_record_time=None, signal_type=None, group=None):
    '''
    Ищет спутники по заданным параметрам.
    Возвращает список имён подходящих спутников и список применённых фильтров.
    '''
    sat_data = json_to_py(cd_sat)  
    res = sat_data
    filter_of = []

    if name is not None:
        res = [sat for sat in res if sat['name'] == name]
        filter_of.append(f"имени '{name}'")

    if norad_id is not None:
        res = [sat for sat in res if sat['norad id'] == norad_id] 
        filter_of.append(f"идентификатору NORAD {norad_id}")

    if frequency is not None:
        res = [sat for sat in res if np.floor(sat['frequency']) == np.floor(frequency)]
        filter_of.append(f"частоте равной {frequency} МГц")

    if min_record_time is not None:
        res = [sat for sat in res if sat['min record time'] == min_record_time] 
        filter_of.append(f"минимальному времени записи {min_record_time} минут")

    if signal_type is not None:
        res = [sat for sat in res if sat['signal type'] == signal_type]
        filter_of.append(f"типу сигнала '{signal_type}'")

    if group is not None:
        res = [sat for sat in res if sat['group'] == group]
        filter_of.append(f"группе '{group}'")

    names = [sat['name'] for sat in res]
    return names, filter_of


def active_names(cd_sat):
    """
    функция возвращает список всех спутников из файла satellites.json
    """
    sat_data = json_to_py(cd_sat)
    names = []

    for sat in sat_data:
        names.append(sat["name"])
    
    return names


def create_urls_to_htpp(cd_sat):
    '''
    создает список url для htpp запросов по всем возможным семействам всех спутников
    '''
    sat_data = json_to_py(cd_sat)
    base = "https://celestrak.org/NORAD/elements/gp.php?NAME="
    form = "&FORMAT=TLE"

    urls = []
    groups = []
    for sat in sat_data:
        if sat['group'] not in groups:
            groups.append(sat['group'])
    
    for name in groups:
        urls.append(base + name + form)

    return urls

def write_or_update_tles(new_tles, cd_tle):
    '''
    на вход в функцию поступает список tles, где в tles[i] - tles[i][0] - имя i-того спутника, 
    tles[i][1] - первая tle строка i-того спутника, tles[i][2] - вторая tle строка i-того спутника, 
    результатом работы функции является обновленный tle.json в формате списка словарей,
    где каждый словарь - строчки tle
    '''
    try:
        tle_json = json_to_py(cd_tle)
    except:
        tle_json = []

    for sat_tle in new_tles:
        if sat_tle[0] not in [sat['name'] for sat in tle_json]:
            tle_json.append({'name': sat_tle[0], 'first tle line': sat_tle[1], 'second tle line': sat_tle[2]})
    
    for sat in tle_json:
        for tle in new_tles:
            if tle[0] == sat['name']: 
                if sat["first tle line"] != tle[1] or sat["second tle line"] != tle[2]:
                    sat["first tle line"] = tle[1]
                    sat["second tle line"] = tle[2]

    with open(cd_tle, 'w') as f:
        json.dump(tle_json, f, indent=4)


def update_calculations(new_calcs, cd_calc):
    '''
    на вход функция принимает список словарей с именем спутника и прочими атрибутами
    Результатом работы функции является обновленный coordinates.json или passes.json
    '''
    json_f = []

    for calc in new_calcs:
        json_f.append(calc)
    
    with open(cd_calc, 'w') as f:
        json.dump(json_f, f, indent = 4)

def write_logs(cd_logs, last_time, next_time):
    last_time_utc = unix_to_utc(last_time)
    next_time_utc = unix_to_utc(next_time)
    logs = (f'В последний раз вычисления обновлялись в {last_time_utc}\n'
            f'Следующее обновление вычислений будет в {next_time_utc}')
    
    with open(cd_logs, 'w', encoding='utf-8') as f:
        f.write(logs)
    

def read_config(cd_config, observer_longitude=True, observer_latitude=True, 
                observer_altitude=True, end_time_hours=True, telegram_bot_token=True,
                venv_name = True):
    '''
    функция читает конфиг и возвращает список с нужными параметрами упорядоченными так же как и сам конфиг
    '''
    config = json_to_py(cd_config)
    out = []
    
    if observer_longitude == True:
        out.append(config.get('observer longitude'))
    
    if observer_latitude == True:
        out.append(config.get('observer latitude'))
    
    if observer_altitude == True:
        out.append(config.get('observer altitude'))
    
    if end_time_hours == True:
        out.append(config.get('calculations for next (hours)'))
    
    if telegram_bot_token == True:
        out.append(config.get('telegram bot token'))
    
    if venv_name == True:
        out.append(config.get('venv name'))
    
    return out

def create_decode_folders_by_names(cd_decode, names):
    for name in names:
        full_path = os.path.join(cd_decode, name + '_decode')
        os.makedirs(full_path, exist_ok=True)
        waw_folder = os.path.join(full_path, 'waw')
        os.makedirs(waw_folder, exist_ok=True)
        img_folder = os.path.join(full_path, 'img')
        os.makedirs(img_folder, exist_ok=True)

def make_path_to_decode_sat(cd_decode, name, waw = False, img = False):
    if waw == True:
        path = os.path.join(cd_decode, 'programm', 'data', 'data_decode', name, 'waw')
    if img == True:
        path = os.path.join(cd_decode, 'programm', 'data', 'data_decode', name, 'img')
    else:
        path = os.path.join(cd_decode, 'programm', 'data', 'data_decode', name)
    return path 

def add_rtl_sdr_libs_to_venv(cd, cd_venv):
    cd_librtlsdr = os.path.join(cd, 'programm', 'decode', 'rlt_sdr_libs', 'librtlsdr.dll')
    cd_libusb = os.path.join(cd, 'programm', 'decode', 'rlt_sdr_libs', 'libusb-1.0.dll')
    cd_venv = os.path.join(cd_venv, 'Scripts')
    if os.path.exists(os.path.join(cd_venv, 'librtlsdr.dll')):
        return None
    if os.path.exists(os.path.join(cd_venv, 'libusb-1.0.dll')):
        return None
    else:
        shutil.copy(cd_librtlsdr, cd_venv)
        shutil.copy(cd_libusb, cd_venv)
