import json
import os

from tracking.parsing import get_not_deb_tle

def json_to_py(cd_json):
    '''Читает json с путем  'cd_json' и возвращает список словарей'''
    with open(cd_json, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def find_satellites(cd_sat, name=None, frequency=None, min_record_time=None, signal_type=None, group=None):
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

def update_calculations_of_coordinates(new_coors, cd_coor):
    '''
    на вход функция принимает список словарей с именем спутника, долготами, широтами, высотами, списком временных точек
    долгот, широт, высот.
    Результатом работы функции является обновленный coordinates.json, где хранятся орбиты спутников,
    привязанные ко времени
    '''
    try:
        coor_json = json_to_py(cd_coor)
    except:
        coor_json = []

    for new_coor in new_coors:
        coor_json.append(new_coor)
    
    with open(cd_coor, 'w') as f:
        json.dump(coor_json, f, indent = 4)