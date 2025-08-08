from skyfield.api import load, utc
from datetime import datetime
import os

from storage import json_to_py, active_names, create_urls_to_htpp
from storage import write_or_update_tles, update_calculations
from tracking.parsing import get_not_deb_tle
from tracking.calculation import calculate_orbit, calculate_samples_from_hours, calculate_passes

def background(obs_lon, obs_lat, obs_alt, end_time_hours):
    cd = os.getcwd() 
    cd_sat = os.path.join(cd, 'programm', 'data', 'data_base', 'satellites.json')
    cd_tle = os.path.join(cd, 'programm', 'data', 'data_base', 'tle.json')
    cd_coordinates = os.path.join(cd, 'programm', 'data', 'data_base', 'coordinates.json')
    cd_passes = os.path.join(cd, 'programm', 'data', 'data_base', 'passes.json')
    last_time_utc_of_calculations = datetime.now(tz=utc)

    samples, step  = calculate_samples_from_hours(end_time_hours)
    sats_tle = json_to_py(cd_tle)

    tles = []
    urls = create_urls_to_htpp(cd_sat)
    '''
    for url in urls:
        tles.append(get_not_deb_tle(url, active_names(cd_sat)))
    for tle_group in tles:
        write_or_update_tles(tle_group, cd_tle)
    '''
    calc_sats = []
    for sat_tle in sats_tle:
        calc_sats.append(calculate_orbit(sat_tle, end_time_hours, samples))

    update_calculations(calc_sats, cd_coordinates)

    calc_passes = []
    for sat_tle in sats_tle:
        calc_passes.append(calculate_passes(sat_tle, end_time_hours, obs_lon, obs_lat, obs_alt))

    update_calculations(calc_passes, cd_passes)
    
    return last_time_utc_of_calculations
