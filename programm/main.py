from skyfield.api import load, EarthSatellite 
import os

from storage import json_to_py, find_satellites, active_names, create_urls_to_htpp, write_or_update_tles, update_calculations_of_coordinates
from tracking.parsing import get_not_deb_tle
from tracking.calculation import calculate_orbit, calculate_samples_from_hours
from tracking.visualization import visualization_orbit_for_one_satellite

ts = load.timescale()
utc_time_now = ts.now().utc_iso().replace('T', ' ').replace('Z', ' UTC')

cd = os.getcwd() 
cd_sat = os.path.join(cd, 'programm', 'data', 'data_base', 'satellites.json')
cd_tle = os.path.join(cd, 'programm', 'data', 'data_base', 'tle.json')
cd_processing = os.path.join(cd, 'programm', 'data', 'data_base', 'processing.json')
cd_coordinates = os.path.join(cd, 'programm', 'data', 'data_base', 'coordinates.json')


#пример кода для обновления tle или добавления новых
tles = []
urls = create_urls_to_htpp(cd_sat)

for url in urls:
    tles.append(get_not_deb_tle(url, active_names(cd_sat)))

for tle_group in tles:
    write_or_update_tles(tle_group, cd_tle)


end_time_hours = 8
samples = calculate_samples_from_hours(end_time_hours)

sats_tle = json_to_py(cd_tle)
calc_sats = []
for sat_tle in sats_tle:
    calc_sats.append(calculate_orbit(sat_tle, end_time_hours, samples))

update_calculations_of_coordinates(calc_sats, cd_coordinates)


tles = json_to_py(cd_tle)

sat_inf = json_to_py(cd_coordinates)
visualization_orbit_for_one_satellite(sat_inf[2], utc_time_now,  37.6155600, 55.7522200)