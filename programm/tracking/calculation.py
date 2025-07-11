import numpy as np
from skyfield.api import load, EarthSatellite 

def calculate_orbit(tle, end_time_hours, samples):
    '''
    функция принимает на вход tle список, где каждый элемент - это новая строка tle, 
    на сколько часов составить прогноз end_ttime_hours, частота дескритищации samples
    возвращает фукнция массив координат (долгота, широта, высота)
    '''
    ts = load.timescale()
    times = ts.now() + np.linspace(0, end_time_hours / 24, samples) 
    satellite = EarthSatellite(tle[1], tle[2], tle[0])

    latitudes = []
    longitudes = []
    elevations = []

    for time in times:
        geocentric = satellite.at(time)
        subpoint = geocentric.subpoint()

        latitudes.append(subpoint.latitude.degrees)
        longitudes.append(subpoint.longitude.degrees)
        elevations.append(subpoint.elevation.km)

    time_utc = ts.now().utc_iso().replace('T', ' ').replace('Z', ' UTC')
    
    sat_coordinates = [tle[0], longitudes, latitudes, elevations, time_utc]
    return sat_coordinates

