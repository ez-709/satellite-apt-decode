import numpy as np
from datetime import datetime, timezone, timedelta

def  julian_time_to_unix(time_julian):
    return [time.utc_datetime().timestamp() for time in time_julian]

def unix_to_utc(time_unix, time_zone = 0):
    return datetime.fromtimestamp(time_unix, tz=timezone(timedelta(hours=time_zone)))

def filter(names, sats):
    '''
    names - список имен спутника
    sats - список словарей, где есть ключи в виде имени спутниика
    '''
    res = []
    for sat in sats:
        if sat['name'] in names:
            res.append(sat)
    
    return res

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

def find_next_passes_for_satellites(time_now, passes, names):
    passes = filter(names, passes)
    time_now = time_now.timestamp()
    next_passes = []
    
    for i in range(len(passes)):
        for time in passes[i]['points']:
            time_rise = time['rise']
            time_culmination = time['culmination']
            time_set = time['set']
            
            if time_set > time_now:  
                if time_rise > time_now:
                    next_passes.append(f"{passes[i]['name']}: rise at {time['rise']}, culmination at {time['culmination']}, set at {time['set']}")
                elif time_culmination > time_now:
                    next_passes.append(f"{passes[i]['name']}: now in the sky, culmination at {time['culmination']}, set at {time['set']}")
                else:
                    next_passes.append(f"{passes[i]['name']}: now in the sky, culmination was at {time['culmination']}, set at {time['set']}")
                break
    
    return next_passes

#интегрировать с функцие посика ближайших пролетов для всех спутников
def find_next_passe(time_now, passes, names):
    passes = filter(names, passes)
    time_now = time_now.timestamp()
    most_closest_time_set = 1e100
    for sat in passes:
        for time in sat['points']:
            time_set = time['set']
            if time_set > time_now and time_set < most_closest_time_set:
                most_closest_time_set = time_set
                most_closest_time_rise = time['rise']
                duration = time['duration (sec)']
                most_closest_sat_name_passe = sat['name']
                
    return most_closest_sat_name_passe, most_closest_time_rise, most_closest_time_set, duration

def check_end_time_hours_correct(time_now_utc, end_time_hour, sats_coordinates):
    time_now_utc = time_now_utc[:19]
    utc_date = datetime.strptime(time_now_utc, '%Y-%m-%d %H:%M:%S')
    new_date = utc_date + timedelta(hours = end_time_hour)
    new_date_string = new_date.strftime('%Y-%m-%d %H:%M:%S UTC')
    new_date_int = new_date_string

    time = sats_coordinates[0]["times in utc"]
    latest_time = time[len(time) - 1]
    
    if new_date_int > latest_time:
        return "Расчет расчитан на меньшее количество часов"
    else:
        return True
    
def find_next_time_for_updating_calculations(last_time_utc_of_calculations, passes):
    for sat in passes:
        for times in sat['points']:
            if utc_to_int(times['rise']) < utc_to_int(last_time_utc_of_calculations):
                continue