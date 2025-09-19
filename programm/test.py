from tracking.utils import sort_passes
from storage import json_to_py
import os

cd = os.getcwd() 
cd_sat = os.path.join(cd, 'programm', 'data', 'data_base', 'satellites.json')
cd_config = os.path.join(cd, 'programm', 'config.json')

cd_tle = os.path.join(cd, 'programm', 'data', 'data_base', 'tle.json')
cd_coordinates = os.path.join(cd, 'programm', 'data', 'data_base', 'coordinates.json')
cd_passes = os.path.join(cd, 'programm', 'data', 'data_base', 'passes.json')
cd_sat_record = os.path.join(cd, 'programm', 'data', 'data_base', 'sat_records.json')

print(sort_passes(json_to_py(cd_passes)))