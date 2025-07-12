import json
import os

from tracking.parsing import get_not_deb_tle

cd = os.getcwd() 
cd_sat = os.path.join(cd, 'programm', 'data', 'data_base', 'satellites.json')
cd_tle = os.path.join(cd, 'programm', 'data', 'data_base', 'tle.json')
cd_processing = os.path.join(cd, 'programm', 'data', 'data_base', 'processing.json')

def json_to_list_of_dicts(cd_json):
    '''Читает json с именем 'name_json" и возвращаtn один единый словарь или список словарей'''
    with open(cd_json, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def find_satellites(name=None, frequency=None, min_record_time=None, signal_type=None, group=None):
    '''
    Фильтрует спутники по заданным параметрам
    Возвращает список словарей с подходящими спутниками
    '''
    sat_data = json_to_list_of_dicts(cd_sat)
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


def create_urls_to_htpp():
    sat_data = json_to_list_of_dicts(cd_sat)
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


tles = [
    ['NOAA 15', '1 25338U 98030A   25192.50463084  .00000165  00000+0  85569-4 0  9998', '2 25338  98.5338 216.8655 0008997 265.1501  94.8653 14.26994957412957'],
    ['NOAA 18', '1 28654U 05018A   25192.47314934  .00000051  00000+0  50383-4 0  9991', '2 28654  98.8422 271.5906 0014877  42.7816 317.4511 14.13617971 38255'],
    ['NOAA 19', '1 33591U 09005A   25192.41396440  .00000145  00000+0  10138-3 0  9990', '2 33591  98.9961 257.2952 0012671 273.8547  86.1176 14.13387759846601'],
    ['NOAA 20 (JPSS-1)', '1 43013U 17073A   25192.48730641  .00000027  00000+0  33532-4 0  9999', '2 43013  98.7410 130.6541 0001302 129.6058 230.5233 14.19544787396139'],
    ['NOAA 21 (JPSS-2)', '1 54234U 22150A   25191.74794225  .00000018  00000+0  29250-4 0  9996', '2 54234  98.7274 130.1716 0002751  84.6320 275.5170 14.19543300138104']
]


def write_or_update_tles(tles):
    '''
    на вход в функцию поступает список tles
    результатом работы функции является обновленный tle.json
    '''
    tle_json = json_to_list_of_dicts(cd_tle)

    for sat_tle in tles:
        if sat_tle[0] not in tle_json:
            tle_json[sat_tle[0]] = sat_tle
    
    for sat in tle_json:
        if tle_json[sat] 
            

    return 

print(write_or_update_tles(tles))