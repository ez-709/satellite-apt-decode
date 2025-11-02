import numpy as np
import os
from skyfield.api import load, EarthSatellite, wgs84, utc
from datetime import datetime, timedelta
import time

from common.utils import julian_time_to_unix, seconds_to_minutes_and_seconds, minutes_and_seconds_to_seconds
from common.storage import json_to_py

def calculate_samples_from_hours(end_time_hours, step = 120): 
    '''
    функция рассчитывает количество семлов от заданого числа часов
    step = 720, то есть шаг равен пяти секундам
    '''
    samples = step * end_time_hours
    return samples, step

def calculate_now_position(sat_tle):
    ts = load.timescale()
    now = ts.now()
    satellite = EarthSatellite(sat_tle['first tle line'], sat_tle["second tle line"], sat_tle["name"])
    geocentric = satellite.at(now)
    subpoint = geocentric.subpoint()
    latitudes = subpoint.latitude.degrees
    longitudes = subpoint.longitude.degrees
    altitude = subpoint.elevation.km
    return longitudes, latitudes, altitude

def calculate_orbit(sat_tle, end_time_hours, samples):
    '''
    функция принимает на вход словарь sat_tle,
    где значения - это строки tle (имя, первая строка tle, вторая строка tle), 
    на сколько часов составить прогноз end_ttime_hours, частота дескритищации samples
    возвращает фукнция словарь, с ключами в виде имени спутника, долгот, широт и списка времени.
    '''
    ts = load.timescale()
    times = ts.now() + np.linspace(0, end_time_hours / 24, samples) 
    times_unix = julian_time_to_unix(times)
    satellite = EarthSatellite(sat_tle['first tle line'], sat_tle["second tle line"], sat_tle["name"])

    latitudes = []
    longitudes = []
    altitude = []

    for time in times:
        geocentric = satellite.at(time)
        subpoint = geocentric.subpoint()

        longitudes.append(subpoint.longitude.degrees)
        latitudes.append(subpoint.latitude.degrees)
        altitude.append(subpoint.elevation.km)
    
    sat_coordinates = {
        'name': sat_tle['name'],
        'longitudes': longitudes,
        'latitudes': latitudes,
        'altitude': altitude,
        'time unix': times_unix
    }
    return sat_coordinates

#поправить чтобы все ключи создавались всегда
def calculate_passes(cd_sat, sat_tle, end_time_hours, obs_longitudes, obs_latitudes, obs_altitude, altitude_degrees=10):
    sats = json_to_py(cd_sat)

    ts = load.timescale()
    now = datetime.now(tz=utc)
    start_time = ts.utc(now)
    end_time = ts.utc(now + timedelta(hours=end_time_hours)) 
    sat = EarthSatellite(sat_tle['first tle line'], sat_tle["second tle line"], sat_tle["name"])
    name = sat_tle['name']
    for s in sats:
        if s['name'] == name:
            min_record_time = s['min record time']

    observer = wgs84.latlon(obs_latitudes, obs_longitudes, obs_altitude)

    times, events = sat.find_events(observer, start_time, end_time, altitude_degrees)
    times_unix = julian_time_to_unix(times)

    points = []
    current_passe = {}
    for i in range(len(times)):
        event_type = int(events[i])
        time_unix = times_unix[i]
        
        if event_type == 0:  
            current_passe = {'rise': time_unix}
        
        elif event_type == 1: 
            latitudes, longitudes, altitude = calculate_now_position(sat_tle)
            difference = sat - observer
            topocentric = difference.at(times[i])
            alt, az, distance = topocentric.altaz()
            angle_above_horizon = alt.degrees
            
            if 'rise' not in current_passe:
                current_passe['rise'] = 1
            current_passe['culmination'] = f'{time_unix} with {str(altitude)[:7]} altitude and {angle_above_horizon} degrees above horizon'
        
        elif event_type == 2:  
            if 'rise' not in current_passe:
                current_passe['rise'] = 1
                
            if 'culmination' in current_passe or 'rise' in current_passe:
                current_passe['set'] = time_unix
                if current_passe['rise'] != 1 and 'set' in current_passe:
                    duration = current_passe['set'] - current_passe['rise']
                    if duration < minutes_and_seconds_to_seconds(min_record_time):
                        current_passe = {}
                        continue
                    else:
                        current_passe['duration (min:sec)'] = seconds_to_minutes_and_seconds(duration)
                else:
                    duration = current_passe['set'] - time.time()
                    if duration < minutes_and_seconds_to_seconds(min_record_time):
                        current_passe = {}
                        continue
                    else:
                        current_passe['duration (min:sec)'] = seconds_to_minutes_and_seconds(duration)
   
                points.append(current_passe)
                current_passe = {} 
            else:
                current_passe['set'] = time_unix

    sat_passe = {
        'name': sat_tle['name'],
        'points': points
    }
    return sat_passe


def calculate_radius_and_coordinates_of_circle(sat_lons, sat_lats, sat_altitude, samples=360, elev_angle_deg = 10):
    r_earth = 6371
    h = sat_altitude
    alpha = np.radians(elev_angle_deg)
    theta = np.arcsin((r_earth * np.cos(alpha)) / (r_earth + h))
    beta = np.pi/2 - alpha - theta
    radius = r_earth * beta
    angular_radius = np.degrees(radius / r_earth)
    angles = np.linspace(0, 2 * np.pi, samples, endpoint=False)
    
    circle_lats = sat_lats + angular_radius * np.sin(angles)
    circle_lons = sat_lons + angular_radius * np.cos(angles) / np.cos(np.radians(sat_lats))
    return radius, circle_lons, circle_lats

