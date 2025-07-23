import datetime
import os
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.feature.nightshade import Nightshade
from skyfield.api import load

from .calculation import calculate_now_position, calculate_radius
from storage import json_to_py

def binary_search_for_utc(time_now, time_utc):
    '''
    функция предназначена для нахождения индекса ближайшего подходящего времени во временном списке utc
    '''
    # надо переписать динарный поиск под более вариационный шаг
    if int(time_now[17:19]) % 10 <= 2 or int(time_now[17:19]) % 10 >= 8:
        sec = str((int(time_now[17:19]) + 5) // 10 * 10)
    else: 
        sec = str((int(time_now[17:19]) + 2) // 5 * 5) 
    if len(sec) != 2:
        sec = '0' + sec
    
    target_time = int(time_now[0:4] + time_now[5:7] + time_now[8:10] + time_now[11:13] + time_now[14:16] + sec)
    right, left = 0, len(time_utc) - 1
    mid = (right + left) // 2
    while right <= left:
        mid = (right + left) // 2
        check_time = int(time_utc[mid][0:4] + time_utc[mid][5:7] + time_utc[mid][8:10] + time_utc[mid][11:13] + time_utc[mid][14:16] + time_utc[mid][17:19])
        if check_time < target_time:
            right = mid + 1
        else:
            left = mid - 1

    return mid

def visualization_orbit_for_satellites(sats, time_now, end_hour, step, lats_obs, lons_obs, print_time = True, print_altitude = True):
    colors = ['g', 'r', 'c', 'm', 'y', 'k', 'b', 'w']

    year, month, day = map(int, time_now.split()[0].split('-'))
    hour, minute, second = map(int, time_now.split()[1].split(':'))
    date = datetime.datetime(year, month, day, hour, minute, second) #cartopy работает только с datetime
    
    plt.figure(figsize=(12, 12))
    ax = plt.axes(projection=ccrs.PlateCarree())
    
    ax.add_feature(cfeature.COASTLINE, linewidth=0.5)
    ax.add_feature(Nightshade(date, alpha=0.3))
    ax.stock_img() 

    ax.gridlines(draw_labels=True, linewidth=0.5, color='gray', alpha=0.5, linestyle='--')
    ax.plot(lons_obs, lats_obs, 'bo', markersize=3, transform=ccrs.PlateCarree(), label='Antenna location')
    if print_time == True:
        ax.plot([], [], 'gx', markersize=0, transform=ccrs.PlateCarree(), label= time_now)

    #отрисовка спутников
    for i in range(len(sats)):
        sat_name = sats[i]['name']
        sat_lons = sats[i]['longitudes']
        sat_lats = sats[i]['latitudes']
        sat_altitude = sats[i]['altitude']
        time_utc = sats[i]['times in utc']

        cd = os.getcwd()
        cd_tle = os.path.join(cd, 'programm', 'data', 'data_base', 'tle.json')
        tles = json_to_py(cd_tle)
        tle = tles[i]
        now_latitudes, now_longitudes, now_altitude = calculate_now_position(tle)

        right = binary_search_for_utc(time_now, time_utc)
        sat_lons = sat_lons[right+1: right + end_hour * step]
        sat_lats = sat_lats[right+1: right + end_hour * step]

        sat_lons.insert(0, now_longitudes)
        sat_lats.insert(0, now_latitudes)
        if print_altitude == True:
            ax.plot(now_longitudes, now_latitudes, f'{colors[i]}*', markersize=5, transform=ccrs.PlateCarree(), label=f'{sat_name}: altitude is {str(now_altitude)[0:7]} km')
        else:
            ax.plot(now_latitudes, now_longitudes, f'{colors[i]}*', markersize=5, transform=ccrs.PlateCarree(), label=f'{sat_name}')
        
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

    plt.legend(
        loc='lower left',          # Якорь легенды в нижнем левом углу
        bbox_to_anchor=(0, 0),     # Фиксированное положение (x=0, y=0)
        fontsize='small',          # Уменьшенный шрифт
        markerscale=0.8,           # Уменьшение размера маркеров
        framealpha=0.4             # Полупрозрачный фон
    )
    plt.title(f'Orbit of satellites for next {end_hour} hours', pad=5)
    
    plt.show()
