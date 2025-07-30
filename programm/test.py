from skyfield.api import load, utc
import os
import numpy as np
from datetime import datetime, timezone, timedelta

from storage import json_to_py, find_satellites, read_config
from tracking.utils import check_end_time_hours_correct
from tracking.calculation import calculate_samples_from_hours
from tracking.visualization import visualization_orbit_for_satellites
from tracking.utils import filter
from background import background

#.utc_iso().replace('T', ' ').replace('Z', ' UTC')

cd = os.getcwd() 
cd_sat = os.path.join(cd, 'programm', 'data', 'data_base', 'satellites.json')
cd_tle = os.path.join(cd, 'programm', 'data', 'data_base', 'tle.json')
cd_processing = os.path.join(cd, 'programm', 'data', 'data_base', 'processing.json')
cd_coordinates = os.path.join(cd, 'programm', 'data', 'data_base', 'coordinates.json')
cd_passes = os.path.join(cd, 'programm', 'data', 'data_base', 'passes.json')
cd_config = os.path.join(cd, 'programm', 'config.json')

ts = load.timescale()
utc_time_now = ts.now().utc_iso().replace('T', ' ').replace('Z', ' UTC')

from datetime import datetime, timezone, timedelta

def unix_to_utc(time_unix, time_zone=12):
    time_str = str(datetime.fromtimestamp(time_unix, tz=timezone(timedelta(hours=time_zone))))
    datetime_part = time_str[:19]
    tz_part = time_str[26:29]
    
    tz_sign = tz_part[0]   
    tz_hours = tz_part[1:].lstrip('0') 

    utc_time = f"{datetime_part} {tz_sign}{tz_hours} UTC"
    return utc_time

print(unix_to_utc(1753848886.287127))

