import os

from storage import json_to_py, find_satellites, active_names, create_urls_to_htpp, write_or_update_tles
from tracking.parsing import get_not_deb_tle
from tracking.calculation import calculate_orbit
from tracking.visualization import visualization_orbit_for_one_satellite


#пример кода для обновления tle или добавления новых
'''tles = []
urls = create_urls_to_htpp()


for url in urls:
    tles.append(get_not_deb_tle(url, active_names()))

for tle in tles:
    write_or_update_tles(tle)'''
cd = os.getcwd() 
cd_sat = os.path.join(cd, 'programm', 'data', 'data_base', 'satellites.json')
cd_tle = os.path.join(cd, 'programm', 'data', 'data_base', 'tle.json')
cd_processing = os.path.join(cd, 'programm', 'data', 'data_base', 'processing.json')

tles = json_to_py(cd_tle)
print(tles["NOAA 15"])


'''sat_inf = calculate_orbit(tles[0], 4, 4000)
visualization_orbit_for_one_satellite(sat_inf, 37.6155600, 55.7522200, print_time = False)'''
