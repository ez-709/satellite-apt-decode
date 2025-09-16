import time
import os

from storage import json_to_py

cd = os.getcwd() 
cd_tle = os.path.join(cd, 'programm', 'data', 'data_base', 'tle.json')
cd_coordinates = os.path.join(cd, 'programm', 'data', 'data_base', 'coordinates.json')
cd_passes = os.path.join(cd, 'programm', 'data', 'data_base', 'passes.json')

data_cache = {
    'coordinates': None,
    'passes': None,
    'tle': None,
    'last_update': 0
}
duration = 24 * 60 * 60  

def get_cached_data():
    global data_cache
    
    if (time.time() - data_cache['last_update']) > duration or data_cache['coordinates'] is None:
        data_cache['coordinates'] = json_to_py(cd_coordinates)
        data_cache['passes'] = json_to_py(cd_passes)
        data_cache['tle'] = json_to_py(cd_tle)
        data_cache['last_update'] = time.time()

    
    return data_cache['coordinates'],  data_cache['tle'],  data_cache['passes']