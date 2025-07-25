import numpy as np
from skyfield.api import load, EarthSatellite, wgs84, utc
from datetime import datetime, timedelta

from .utils import calculate_delta_time_utc

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
    satellite = EarthSatellite(sat_tle['first tle line'], sat_tle["second tle line"], sat_tle["name"])

    latitudes = []
    longitudes = []
    altitude = []
    times_utc = []

    for time in times:
        geocentric = satellite.at(time)
        subpoint = geocentric.subpoint()

        latitudes.append(subpoint.latitude.degrees)
        longitudes.append(subpoint.longitude.degrees)
        altitude.append(subpoint.elevation.km)
        times_utc.append(time.utc_iso().replace('T', ' ').replace('Z', ' UTC'))
    
    
    sat_coordinates = {
        'name': sat_tle['name'],
        'longitudes': longitudes,
        'latitudes': latitudes,
        'altitude': altitude,
        'times in utc': times_utc 
    }
    return sat_coordinates


def calculate_passes(sat_tle, end_time_hours, obs_latitudes, obs_longitudes, obs_altitude, altitude_degrees=10.0):
    ts = load.timescale()
    now = datetime.now(tz=utc)
    start_time = ts.utc(now)
    end_time = ts.utc(now + timedelta(hours=end_time_hours)) 
    sat = EarthSatellite(sat_tle['first tle line'], sat_tle["second tle line"], sat_tle["name"])

    observer = wgs84.latlon(obs_latitudes, obs_longitudes, obs_altitude)

    times, events = sat.find_events(observer, start_time, end_time, altitude_degrees)

    points = []
    current_passe = {}
    
    for i in range(len(times)):
        time = times[i].utc_iso().replace('T', ' ').replace('Z', ' UTC')
        event_type = int(events[i])
        
        if event_type == 0:  
            current_passe = {'rise': time}
        elif event_type == 1: 
            latitudes, longitudes, altitude = calculate_now_position(sat_tle)
            if 'rise' in current_passe:
                current_passe['culmination'] = f'{time} with {str(altitude)[:7]} altitude'
            else:
                current_passe = {'culmination': f'{time} with {str(altitude)[:7]} altitude'}
        elif event_type == 2:  
            if 'culmination' in current_passe or 'rise' in current_passe:
                current_passe['set'] = time
                if 'rise' in current_passe and 'set' in current_passe:
                    current_passe['duration (sec)'] = calculate_delta_time_utc(current_passe['rise'], current_passe['set'])
                points.append(current_passe)
                current_passe = {} 
            else:
                current_passe = {'set': time}

    sat_passe = {
        'name': sat_tle['name'],
        'points': points
    }
    return sat_passe


def calculate_radius_and_coordinates_of_circle(sat_lons, sat_lats, sat_altitude, samples=360):
    r_earth = 6371
    
    radius = np.sqrt((r_earth + sat_altitude)**2 - r_earth**2) * 0.7
    
    angular_radius = np.degrees(radius / r_earth) 
    
    angles = np.linspace(0, 2 * np.pi, samples, endpoint=False)
    
    circle_lats = sat_lats + angular_radius * np.sin(angles)
    circle_lons = sat_lons + angular_radius * np.cos(angles) / np.cos(np.radians(sat_lats))
    
    return radius, circle_lons, circle_lats

