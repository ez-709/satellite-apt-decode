import datetime
import os
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.feature.nightshade import Nightshade

from .calculation import calculate_now_position, calculate_radius_and_coordinates_of_circle
from .utils import binary_search_for_utc, utc_to_int, find_next_passe
from storage import json_to_py


def visualization_orbit_for_satellites(sats, time_now, end_hour, step, lons_obs, lats_obs, elevation_obs, print_time = True, print_altitude = True):
    #для работы с бд
    cd = os.getcwd()
    cd_tle = os.path.join(cd, 'programm', 'data', 'data_base', 'tle.json')
    cd_passes = os.path.join(cd, 'programm', 'data', 'data_base', 'passes.json')
    tles = json_to_py(cd_tle)
    passes = json_to_py(cd_passes)
    colors = ['g', 'r', 'c', 'm', 'y', 'k', 'b', 'w']

    year, month, day = map(int, time_now.split()[0].split('-'))
    hour, minute, second = map(int, time_now.split()[1].split(':'))
    date = datetime.datetime(year, month, day, hour, minute, second) #cartopy работает только с datetime
    
    plt.figure(figsize=(12, 12))
    ax = plt.axes(projection=ccrs.PlateCarree())
    #параметры карты
    ax.add_feature(cfeature.COASTLINE, linewidth=0.5)
    ax.add_feature(Nightshade(date, alpha=0.3))
    ax.stock_img() 
    ax.gridlines(draw_labels=True, linewidth=0.5, color='gray', alpha=0.5, linestyle='--')

    #отрисовка вспомогательных элементов
    ax.plot(lons_obs, lats_obs, 'bo', markersize=3, transform=ccrs.PlateCarree(), label='Antenna location')

    if print_time == True:
        ax.plot([], [], 'gx', markersize=0, transform=ccrs.PlateCarree(), label= time_now)
    
    #поиск ближайшего пролета
    most_closest_sat_name_passe, most_closest_time_rise, most_closest_time_set, duration = find_next_passe(time_now, passes)

    #отрисовка спутников
    for i in range(len(sats)):
        sat_name = sats[i]['name']
        sat_lons = sats[i]['longitudes']
        sat_lats = sats[i]['latitudes']
        sat_altitude = sats[i]['altitude']
        time_utc = sats[i]['times in utc']
        
        for tle in tles:
            if tle['name'] == sat_name:
                break
        now_longitudes, now_latitudes, now_altitude = calculate_now_position(tle)
        
        
        right = binary_search_for_utc(time_now, time_utc)
        #провера на коректный срез крайней точки
        if utc_to_int(time_now) < utc_to_int(time_utc[right]):
            sat_lons = sat_lons[right: right + end_hour * step]
            sat_lats = sat_lats[right: right + end_hour * step]
        else:
            sat_lons = [now_longitudes] + sat_lons[right+1: right + end_hour * step]
            sat_lats = [now_latitudes] + sat_lats[right+1: right + end_hour * step]

        if print_altitude == True:
            ax.plot(now_longitudes, now_latitudes, f'{colors[i]}*', markersize=5, transform=ccrs.PlateCarree(), label=f'{sat_name}: altitude is {str(now_altitude)[0:7]} km')
        else:
            ax.plot(now_longitudes, now_latitudes, f'{colors[i]}*', markersize=5, transform=ccrs.PlateCarree(), label=f'{sat_name}')
        
        #решение проблемы отрисовки горизонтальных линий
        sector_lons = []
        sector_lats = []
        for x in range(0, len(sat_lons)):
            if np.abs(sat_lons[x] - sat_lons[x-1]) > 180:
                ax.plot(sector_lons, sector_lats, f'{colors[i]}-', linewidth=0.8, transform=ccrs.PlateCarree())
                sector_lons = []
                sector_lats = []
                
            else:
                sector_lons.append(sat_lons[x])
                sector_lats.append(sat_lats[x])

        # отрисовка зоны видимости        
        if most_closest_sat_name_passe == sat_name:
            radius, circle_lons, circle_lats = calculate_radius_and_coordinates_of_circle(lons_obs, lats_obs, elevation_obs, now_altitude)

            ax.plot(circle_lons, circle_lats, f'{colors[i]}-', markersize=1, transform=ccrs.PlateCarree(), label = 'Instantaneous Visibility Zone' )
            ax.plot([], [], f'{colors[i]}*', markersize=0, transform=ccrs.PlateCarree(), label= f'rise in {most_closest_time_rise}')
            ax.plot([], [], f'{colors[i]}*', markersize=0, transform=ccrs.PlateCarree(), label= f'set in {most_closest_time_set}')
            ax.plot([], [], f'{colors[i]}*', markersize=0, transform=ccrs.PlateCarree(), label= f'durationn is {duration} sec')

    plt.legend(
        loc='lower left',          # Якорь легенды в нижнем левом углу
        bbox_to_anchor=(0, 0),     # Фиксированное положение (x=0, y=0)
        fontsize='small',          # Уменьшенный шрифт
        markerscale=0.8,           # Уменьшение размера маркеров
        framealpha=0.4             # Полупрозрачный фон
    )
    plt.title(f'Orbit of satellites for next {end_hour} hours', pad=5)
    
    plt.show()
