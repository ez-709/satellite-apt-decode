import json
import os

from tracking.parsing import get_not_deb_tle

cd = os.getcwd() 
cd_sat = os.path.join(cd, 'programm', 'data', 'data_base', 'satellites.json')
cd_tle = os.path.join(cd, 'programm', 'data', 'data_base', 'tle.json')
cd_processing = os.path.join(cd, 'programm', 'data', 'data_base', 'processing.json')

def json_to_py(cd_json):
    '''Читает json с именем 'name_json" и возвращаtn один единый словарь или список словарей'''
    with open(cd_json, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def find_satellites(name=None, frequency=None, min_record_time=None, signal_type=None, group=None):
    '''
    Фильтрует спутники по заданным параметрам
    Возвращает список словарей с подходящими спутниками
    '''
    sat_data = json_to_py(cd_sat)
    res = sat_data 
    
    if name is not None:
        res = [sat for sat in res if sat['name'] == name]
    
    if frequency is not None:
        res = [sat for sat in res if sat['frequency'] == frequency]
    
    if min_record_time is not None:
        res = [sat for sat in res if sat['min_record_time'] == min_record_time]
    
    if signal_type is not None:
        res = [sat for sat in res if sat['signal_type'] == signal_type]
    
    if group is not None:
        res = [sat for sat in res if sat['group'] == group]
    
    return res

def active_names():
    """
    функция возвращает список всех спутников из файла satellites.json
    """
    sat_data = json_to_py(cd_sat)
    names = []

    for sat in sat_data:
        names.append(sat["name"])
    
    return names


def create_urls_to_htpp():
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

def write_or_update_tles(new_tles):
    '''
    на вход в функцию поступает список tles
    результатом работы функции является обновленный tle.json
    '''
    try:
        tle_json = json_to_py(cd_tle)
    except:
        tle_json = {}

    for sat_tle in new_tles:
        if sat_tle[0] not in tle_json:
            tle_json[sat_tle[0]] = sat_tle
    
    for sat in tle_json:
        for tle in new_tles:
            if sat == tle[0]:
                if tle_json[sat][0] != tle[1] or tle_json[sat][1] != tle[2]:
                    tle_json[sat] = [tle[1], tle[2]]
    
    with open(cd_tle, 'w') as f:
        json.dump(tle_json, f, indent=4)


