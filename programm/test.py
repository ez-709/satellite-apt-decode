import os

from tracking.utils import find_next_passes_for_satellites
from storage import json_to_py

cd = os.getcwd() 
cd_sat = os.path.join(cd, 'programm', 'data', 'data_base', 'satellites.json')
cd_tle = os.path.join(cd, 'programm', 'data', 'data_base', 'tle.json')
cd_processing = os.path.join(cd, 'programm', 'data', 'data_base', 'processing.json')
cd_coordinates = os.path.join(cd, 'programm', 'data', 'data_base', 'coordinates.json')
cd_passes = os.path.join(cd, 'programm', 'data', 'data_base', 'passes.json')
cd_config = os.path.join(cd, 'programm', 'config.json')

def minutes_and_seconds_to_seconds(time):
    '''
    time - 'minutes:seconds'
    '''
    minutes, seconds = [int(i) for i in time.split(':')]
    return minutes * 60 + seconds

def seconds_to_minutes_and_seconds(seconds):
    minutes = seconds // 60
    seconds = seconds % 60
    return str(minutes) + ':' + str(seconds)

print(minutes_and_seconds_to_seconds('5:20'))
print(seconds_to_minutes_and_seconds(320))