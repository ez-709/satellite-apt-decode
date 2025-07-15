import numpy as np
from skyfield.api import load, EarthSatellite 

def calculate_orbit(sat_tle, end_time_hours, samples):
    '''
    функция принимает на вход словарь sat_tle,
    где значения - это строки tle (имя, первая строка tle, вторая строка tle), 
    на сколько часов составить прогноз end_ttime_hours, частота дескритищации samples
    возвращает фукнция словарь, где ключ - имя спутника, а значение -  список списокв
    долгот, широт, высот, список временных точке
    '''
    ts = load.timescale()
    times = ts.now() + np.linspace(0, end_time_hours / 24, samples) 
    satellite = EarthSatellite(sat_tle['first tle line'], sat_tle["second tle line"], sat_tle["name"])

    latitudes = []
    longitudes = []
    elevations = []
    times_utc = []

    for time in times:
        geocentric = satellite.at(time)
        subpoint = geocentric.subpoint()

        latitudes.append(subpoint.latitude.degrees)
        longitudes.append(subpoint.longitude.degrees)
        elevations.append(subpoint.elevation.km)
        times_utc.append(time.utc_iso().replace('T', ' ').replace('Z', ' UTC'))
    
    
    sat_coordinates = {
        'name': sat_tle['name'],
        'longitudes': longitudes,
        'latitudes': latitudes,
        'elevations': elevations,
        'times in utc': times_utc 
    }
    return sat_coordinates

def calculate_samples_from_hours(end_time_hours, step = 720): 
    '''
    функция рассчитывает количество семлов от заданого числа часов
    step = 720, то есть шаг равен пяти секундам
    '''
    samples = step * end_time_hours
    return samples, step

def calculate_radius_of_satellite_reception(sat_elev, lons_obs, lats_obs, angle  = 10):
    angle = angle * 180 / np.pi

    
