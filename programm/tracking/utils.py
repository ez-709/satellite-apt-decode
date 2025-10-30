import os
from datetime import datetime, timezone, timedelta
import time

def  julian_time_to_unix(time_julian):
    return [time.utc_datetime().timestamp() for time in time_julian]

def unix_to_utc(time_unix, time_zone = 3):
    time_str = str(datetime.fromtimestamp(time_unix, tz=timezone(timedelta(hours=time_zone))))
    datetime_part = time_str[:19]
    tz_part = time_str[26:29]
    tz_sign = tz_part[0]   
    tz_hours = tz_part[1:].lstrip('0') 

    utc_time = f"{datetime_part} {tz_sign}{tz_hours} UTC"
    return utc_time

def filter_by_names(names, sats):
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
    minutes = int(seconds // 60)
    seconds = round(seconds % 60)
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
    
def find_next_passes_for_satellites(passes, names):
    passes = filter_by_names(names, passes)
    time_now = time.time()
    next_passes = []
    
    for i in range(len(passes)):
        for time_point in passes[i]['points']:
            time_rise = time_point['rise']
            if 'culmination' in time_point:
                time_culmination = float(str(time_point['culmination']).split()[0])
                angle = round(float(str(time_point['culmination']).split()[5]))
            time_set = time_point['set']
            duration = time_point['duration (min:sec)']
            
            if time_set > time_now:  
                if time_rise > time_now:
                    next_passes.append((f"Ближайший пролет у {passes[i]['name']}:\n"
                                        f"  восход в {unix_to_utc(time_rise)}\n"
                                        f"  кульминация в {unix_to_utc(time_culmination)}\n"
                                        f"  угол над горизонтом в момент кульминации: {angle} градусов\n"
                                        f"  заход в {unix_to_utc(time_set)}\n"
                                        f"  продолжительность: {duration} (мин:сек)\n"
                                        ))
                elif time_culmination > time_now:
                    time_left = time_set - time_now
                    next_passes.append((f"{passes[i]['name']} сейчас над головой\n"
                                        f"  кульминация в {unix_to_utc(time_culmination)}\n"
                                        f"  угол над горизонтом в момент кульминации: {angle} градусов\n"
                                        f"  заход в {unix_to_utc(time_set)}\n"
                                        f"  осталось до конца: {seconds_to_minutes_and_seconds(time_left)} (мин:сек)\n"
                                        ))
                else:
                    time_left = time_set - time_now
                    next_passes.append((f"{passes[i]['name']} сейчас над головой\n"
                                        f"  кульминация была в {unix_to_utc(time_culmination)}\n"
                                        f"  угол над горизонтом в момент кульминации: {angle} градусов\n"
                                        f"  заход в {unix_to_utc(time_set)}\n"
                                        f"  осталось до конца: {seconds_to_minutes_and_seconds(time_left)} (мин:сек)\n"
                                        ))
                break

    next_passes.sort(key=lambda x: x.split('в ')[1].split('\n')[0])

    return next_passes

def find_next_passes_for_one_satellite(name, passes):
    filtered_passes = filter_by_names([name], passes)
    
    time_now = time.time()
    next_passes = []

    for time_point in filtered_passes[0].get('points', []):
        time_rise = time_point['rise']
        culmination_parts = str(time_point['culmination']).split()
        time_culmination = float(culmination_parts[0])
        angle = round(float(culmination_parts[5])) 
        time_set = time_point['set']
        duration = time_point['duration (min:sec)']
        
        if time_set > time_now:  
            if time_rise > time_now:
                next_passes.append(
                    f"{name}:\n"
                    f" восход в {unix_to_utc(time_rise)}\n"
                    f" кульминация в {unix_to_utc(time_culmination)}\n"
                    f" угол над горизонтом в момент кульминации: {angle} градусов\n"
                    f" заход в {unix_to_utc(time_set)}\n"
                    f" продолжительность: {duration} (мин:сек)"
                )
            elif time_culmination > time_now:
                time_left = time_set - time_now
                next_passes.append(
                    f"{name}:\n"
                    f" сейчас над головой\n"
                    f" кульминация в {unix_to_utc(time_culmination)}\n"
                    f" угол над горизонтом в момент кульминации: {angle} градусов\n"
                    f" заход в {unix_to_utc(time_set)}\n"
                    f" осталось до конца: {seconds_to_minutes_and_seconds(time_left)} (мин:сек)"
                )
            else:
                time_left = time_set - time_now
                next_passes.append(
                    f"{name}:\n"
                    f" сейчас над головой\n"
                    f" кульминация была в {unix_to_utc(time_culmination)}\n"
                    f" угол над горизонтом в момент кульминации: {angle} градусов\n"
                    f" заход в {unix_to_utc(time_set)}\n"
                    f" осталось до конца: {seconds_to_minutes_and_seconds(time_left)} (мин:сек)"
                )
            
    return next_passes[:4]
    
def check_end_time_hours_correct(time_now_unix, end_time_hour, sats_coordinates):
    end_time_unix = time_now_unix + end_time_hour * 3600
    times = sats_coordinates[0]["time unix"] 
    latest_time_unix = times[-1] 
    
    if end_time_unix > latest_time_unix:
        return "Расчет рассчитан на меньшее количество часов"
    else:
        return True
    
def find_next_time_for_updating_calculations(last_time_unix_of_calculations, passes):
    from storage import write_logs
    
    next_time_unix = last_time_unix_of_calculations + 24 * 60 * 60
    min_gap = 122
    events = []
    cd = os.getcwd()
    cd_logs_back = os.path.join(cd, 'programm', 'data','logs', 'logs_back.txt')
    
    for sat in passes:
        for point in sat['points']:
            events.append((point['rise'], point['set']))

    events.sort(key=lambda x: x[0])

    result = None

    for rise, set_ in events:
        if rise <= next_time_unix <= set_:
            log_message = f"Ветка 1: внутри пролёта (начало: {unix_to_utc(rise)}, конец: {unix_to_utc(set_)}), перенос на {set_ + 5 - next_time_unix} сек\n"
            write_logs(cd_logs_back, log_message, update=True)
            result = set_ + 5
            return result

    if result is None:
        if next_time_unix + min_gap <= events[0][0]:
            log_message = "Ветка 2: окно до первого пролёта, перенос не нужен\n"
            write_logs(cd_logs_back, log_message, update=True)
            result = next_time_unix
            return result
        else:
            for i in range(len(events) - 1):
                if events[i][1] <= next_time_unix <= events[i+1][0] - min_gap:
                    log_message = f"Ветка 3: уже между пролётами (конец {unix_to_utc(events[i][1])} - начало {unix_to_utc(events[i+1][0])}), перенос не нужен\n"
                    write_logs(cd_logs_back, log_message, update=True)
                    result = next_time_unix
                    return result

                if events[i][1] > next_time_unix and events[i][1] + min_gap <= events[i+1][0]:
                    log_message = f"Ветка 4: ждём до конца пролёта (конец: {unix_to_utc(events[i][1])}), перенос на {events[i][1] + 5 - next_time_unix} сек\n"
                    write_logs(cd_logs_back, log_message, update=True)
                    result = events[i][1] + 5
                    return result

            if next_time_unix >= events[-1][1]:
                log_message = "Ветка 5: после всех пролётов, перенос не нужен\n"
                write_logs(cd_logs_back, log_message, update=True)
                result = next_time_unix
                return result
            else:
                log_message = f"Ветка 6: резервная, перенос на {events[-1][1] + 5 - next_time_unix} сек\n"
                write_logs(cd_logs_back, log_message, update=True)
                result = events[-1][1] + 5
                return result
            
import time

def sort_passes(passes):
    sorted_passes = []
    current_time = time.time()
    for satellite in passes:
        name = satellite['name']
        for point in satellite['points']:
            if current_time < point['rise']:
                sorted_passes.append({
                    'name': name,
                    'rise': point['rise'],
                    'duration': point['duration (min:sec)'],
                })
    sorted_passes.sort(key=lambda x: x['rise'])
    return sorted_passes