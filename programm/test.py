from skyfield.api import load, utc
import os
import numpy as np
from datetime import datetime

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



coor = json_to_py(cd_coordinates)
times = coor[0]['unix times']


def binary_search(target_time, times_unix):
    '''
    Функция для нахождения индекса ближайшего времени в отсортированном списке times_unix.
    Возвращает индекс элемента с наименьшей разницей с целевым временем.
    '''
    left, right = 0, len(times_unix) - 1
    most_closest_index = 0
    min_diff = float('inf')

    while left <= right:
        mid = (right + left) // 2
        current_time = times_unix[mid]
        current_diff = abs(current_time - target_time)

        if current_diff < min_diff:
            min_diff = current_diff
            most_closest_index = mid

        if current_time == target_time:
            return mid
        elif target_time < current_time:
            right = mid - 1
        else:
            left = mid + 1
            
    candidates = [most_closest_index]
    if most_closest_index > 0:
        candidates.append(most_closest_index - 1)
    if most_closest_index < len(times_unix) - 1:
        candidates.append(most_closest_index + 1)

    for i in candidates:
        current_diff = abs(times_unix[i] - target_time)
        if current_diff < min_diff:
            min_diff = current_diff
            most_closest_index = i

    return most_closest_index

print(times[binary_search(1754002914.642232, times)])