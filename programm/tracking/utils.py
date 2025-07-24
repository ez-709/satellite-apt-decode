import numpy as np
from datetime import datetime

def utc_to_int(time, sec = True):
    '''
    функция принимает на вход время в формате utc: "2025-07-24 08:40:39 UTC"
    фвозращает int 20250724084039, что потом удобно для сравнения дат
    '''
    if sec == True:
        time = int(time[0:4] + time[5:7] + time[8:10] + time[11:13] + time[14:16] + time[17:19])
    else:
        time = int(time[0:4] + time[5:7] + time[8:10] + time[11:13] + time[14:16])
    
    return time

def int_to_utc(time):
    '''
    функция принимает на вход время в формате int: int 20250724084039
    возращает str "2025-07-24 08:40:39 UTC"
    '''
    time = str(time)
    return f"{time[0:4]}-{time[4:6]}-{time[6:8]} {time[8:10]}:{time[10:12]}:{time[12:14]} UTC"

def calculate_delta_time_utc(time_1, time_2):
    '''
    фукнция считает 
    '''
    time_1 = datetime.strptime(time_1[:19], "%Y-%m-%d %H:%M:%S")
    time_1_unix = int(time_1.timestamp())
    time_2 = datetime.strptime(time_2[:19],  "%Y-%m-%d %H:%M:%S")
    time_2_unix = int(time_2.timestamp())
    return time_2_unix - time_1_unix

def binary_search_for_utc(time, times_utc):
    '''
    Функция для нахождения индекса ближайшего времени в отсортированном списке times_utc.
    Возвращает индекс элемента с наименьшей разницей с целевым временем.
    '''
    left, right = 0, len(times_utc) - 1
    target_time = utc_to_int(time, sec=True)
    most_closest_index = 0
    min_diff = float('inf')

    while left <= right:
        mid = (right + left) // 2
        current_time = utc_to_int(times_utc[mid])
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
    if most_closest_index < len(times_utc) - 1:
        candidates.append(most_closest_index + 1)

    for i in candidates:
        current_diff = abs(utc_to_int(times_utc[i]) - target_time)
        if current_diff < min_diff:
            min_diff = current_diff
            most_closest_index = i

    return most_closest_index

def find_next_passe(time_now, passes):
    time_now = utc_to_int(time_now)

    most_closest_time_rise = 1e100
    for sat in passes:
        for time in sat['points']:
            time_rise = utc_to_int(time['rise'])
            if time_rise > time_now and time_rise < most_closest_time_rise:
                most_closest_time_rise = time_rise
                most_closest_time_set = time['set']
                duration = time['duration (sec)']
                most_closest_sat_name_passe = sat['name']
    return most_closest_sat_name_passe, int_to_utc(most_closest_time_rise), most_closest_time_set, duration