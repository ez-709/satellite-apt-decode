import json
import numpy as np

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
        filter_of.append(f'name is {name}')

    if norad_id is not None:
        res = [sat for sat in res if sat['norad id'] == norad_id] 
        filter_of.append(f'norad id is {norad_id}')

    if frequency is not None:
        res = [sat for sat in res if np.floor(sat['frequency']) == np.floor(frequency)]
        filter_of.append(f'frequency ≈ {frequency} MHz')

    if min_record_time is not None:
        res = [sat for sat in res if sat['min record time'] == min_record_time] 
        filter_of.append(f'min record time is {min_record_time} minutes')

    if signal_type is not None:
        res = [sat for sat in res if sat['signal type'] == signal_type]
        filter_of.append(f'signal type is {signal_type}')

    if group is not None:
        res = [sat for sat in res if sat['group'] == group]
        filter_of.append(f'group is {group}')

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

def read_config(cd_config, observer_longitude=True, observer_latitude=True, observer_altitude=True, end_time_hours=True, telegram_bot_token=True):
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
    
    return out