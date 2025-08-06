
import os
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from datetime import datetime
from skyfield.api import load
from cartopy.feature.nightshade import Nightshade

from .calculation import calculate_now_position, calculate_radius_and_coordinates_of_circle
from .utils import binary_search, find_next_passe, unix_to_utc
from storage import json_to_py


def visualization_orbit_for_satellites(sats, time_now_unix, end_hour, step, lons_obs, lats_obs, names, filter_of = True, print_time = True, print_altitude = True, visible = True):
    #для работы с бд
    cd = os.getcwd()
    cd_tle = os.path.join(cd, 'programm', 'data', 'data_base', 'tle.json')
    cd_passes = os.path.join(cd, 'programm', 'data', 'data_base', 'passes.json')
    tles = json_to_py(cd_tle)
    passes = json_to_py(cd_passes)
    colors = ["#D40A0A", "#F1B501", "#007034", "#2800BA", '#A23B72', "#00DCBF", "#000000", "#803A0F", "#8C8C8C", "#691D3F", '#D68FD6']

    ts = load.timescale()
    time_now_utc = ts.now().utc_datetime()
    
    plt.figure(figsize=(12, 12))
    ax = plt.axes(projection=ccrs.PlateCarree())
    #параметры карты
    ax.add_feature(Nightshade(time_now_utc, alpha=0.3))
    ax.add_feature(cfeature.LAND)
    ax.add_feature(cfeature.OCEAN)
    ax.add_feature(cfeature.COASTLINE, linewidth=0.5)
    ax.add_feature(cfeature.BORDERS, linestyle=':', linewidth=0.5)
    ax.add_feature(cfeature.LAKES, alpha=0.5)
    ax.add_feature(cfeature.RIVERS, linewidth=0.5)
    #ax.stock_img() 
    ax.gridlines(draw_labels=True, linewidth=0.5, color='gray', alpha=0.5, linestyle='--')

    #отрисовка вспомогательных элементов
    if print_time == True:
        ax.plot([], [], 'gx', markersize=0, transform=ccrs.PlateCarree(), label= unix_to_utc(time_now_unix))
    ax.plot([], [], 'gx', markersize=0, transform=ccrs.PlateCarree(),label = 'Circles show where satellite is visible')
    
    ax.plot(lons_obs, lats_obs,  'o', color = 'black', markersize=3, transform=ccrs.PlateCarree(), label='Antenna location')
    #поиск ближайшего пролета
    most_closest_sat_name_passe, most_closest_time_rise, most_closest_time_set, duration = find_next_passe(time_now_unix, passes, names)
    minutes_duration, seconds_duration = [int(i) for i in duration.split(':')]

    #отрисовка спутников
    for i in range(len(sats)):
        sat_name = sats[i]['name']
        sat_lons = sats[i]['longitudes']
        sat_lats = sats[i]['latitudes']
        sat_altitude = sats[i]['altitude']
        time_unix = sats[i]['time unix']
        
        for tle in tles:
            if tle['name'] == sat_name:
                break
        now_longitudes, now_latitudes, now_altitude = calculate_now_position(tle)
        
        right = binary_search(time_now_unix, time_unix)
        #провера на коректный срез крайней точки
        if time_now_unix < time_unix[right]:
            sat_lons = sat_lons[right: right + end_hour * step]
            sat_lats = sat_lats[right: right + end_hour * step]
        else:
            sat_lons = [now_longitudes] + sat_lons[right+1: right + end_hour * step]
            sat_lats = [now_latitudes] + sat_lats[right+1: right + end_hour * step]

        #отрисовка зоны где сейчас наблюдается спутник
        if visible == True:
            radius, circle_lons, circle_lats = calculate_radius_and_coordinates_of_circle(now_longitudes, now_latitudes, now_altitude)
            ax.plot(circle_lons, circle_lats, '-', color = colors[i], linewidth=0.8, transform=ccrs.PlateCarree())

        #отображение, что следующий пролет у данного спутника  
        if most_closest_sat_name_passe == sat_name:
            if print_altitude == True:
                ax.plot(now_longitudes, now_latitudes, '*', color = colors[i], markersize=5, transform=ccrs.PlateCarree(), label=f'Next passe of {sat_name}: altitude is {str(now_altitude)[0:3]} km')
            else:
                ax.plot(now_longitudes, now_latitudes, '*', color = colors[i], markersize=5, transform=ccrs.PlateCarree(), label=f'Next passe of {sat_name}')
            
            ax.plot([], [],  '*', color = colors[i], markersize=0, transform=ccrs.PlateCarree(), label= f'rise in {unix_to_utc(most_closest_time_rise)}')
            ax.plot([], [],  '*', color = colors[i], markersize=0, transform=ccrs.PlateCarree(), label= f'set in {unix_to_utc(most_closest_time_set)}')
            ax.plot([], [],  '*', color = colors[i], markersize=0, transform=ccrs.PlateCarree(), label= f'duration {minutes_duration} min. {seconds_duration} sec.')

        else:
            if print_altitude == True:
                ax.plot(now_longitudes, now_latitudes, '*', color = colors[i], markersize=5, transform=ccrs.PlateCarree(), label=f'{sat_name}: altitude is {str(now_altitude)[0:3]} km')
            else:
                ax.plot(now_longitudes, now_latitudes, '*', color = colors[i], markersize=5, transform=ccrs.PlateCarree(), label=f'{sat_name}')
        
        #решение проблемы отрисовки горизонтальных линий
        sector_lons = []
        sector_lats = []
        for x in range(0, len(sat_lons)):
            if np.abs(sat_lons[x] - sat_lons[x-1]) > 180:
                ax.plot(sector_lons, sector_lats,  '-', color = colors[i], linewidth=1, transform=ccrs.PlateCarree())
                sector_lons = []
                sector_lats = []
                
            else:
                sector_lons.append(sat_lons[x])
                sector_lats.append(sat_lats[x])
    

    plt.legend(
        loc='lower left',          # Якорь легенды в нижнем левом углу
        bbox_to_anchor=(0, 0),     # Фиксированное положение (x=0, y=0)
        fontsize='x-small',          # Уменьшенный шрифт
        markerscale=0.6,           # Уменьшение размера маркеров
        framealpha=0.6             # Полупрозрачный фон
    )
    if filter_of == True and len(sats) > 1:
        plt.title(f'Satellites orbits for next {end_hour} hours filtered by {", ".join(str(el) for el in filter_of)}', pad=5)
    elif len(sats) == 1:
        name = sats[0]['name']
        plt.title(f'{name} orbits for next {end_hour} hours', pad=5)
    else:
        plt.title(f'Satellites orbits for next {end_hour} hours', pad=5)
    
    plt.show()
