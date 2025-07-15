import numpy as np
import matplotlib.pyplot as plt
import datetime

import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.feature.nightshade import Nightshade

def visualization_orbit_for_one_satellite(sat_coordinates, time_now, end_hour, step, lons_obs, lats_obs, print_time = True, print_elevation = True, color = 'r'):

    sat_name = sat_coordinates['name']
    sat_lons = sat_coordinates['longitudes']
    sat_lats = sat_coordinates['latitudes']
    sat_elev = sat_coordinates['elevations']
    time_utc = sat_coordinates['times in utc']

    if time_now[:10] == time_utc[0][:10]:
        target_time = int(time_now[11:13]+ time_now[14:16])
        right, left = 0, len(time_utc) - 1
        mid = (right + left) // 2

        while right <= left:
            mid = (right + left) // 2
            check_time = int(time_utc[mid][11:13] + time_utc[mid][14:16])
            if check_time < target_time:
                right = mid + 1
            else:
                left = mid - 1
    else:
        return "Расчеты орбит устарели"
    
    sat_lons = sat_lons[mid: end_hour * step]
    sat_lats = sat_lats[mid: end_hour * step]

    year, month, day = map(int, time_now.split()[0].split('-'))
    hour, minute, second = map(int, time_now.split()[1].split(':'))
    date = datetime.datetime(year, month, day, hour, minute, second) #cartopy работает только с datetime
    
    plt.figure(figsize=(12, 12))
    ax = plt.axes(projection=ccrs.PlateCarree())
    
    ax.add_feature(cfeature.COASTLINE, linewidth=0.5)
    ax.add_feature(Nightshade(date, alpha=0.3))
    ax.stock_img() 

    ax.gridlines(draw_labels=True, linewidth=0.5, color='gray', alpha=0.5, linestyle='--')

    ax.plot(sat_lons[0], sat_lats[0], f'{color}*', markersize=5, transform=ccrs.PlateCarree(), label=f'{sat_name} now')
    ax.plot(lons_obs, lats_obs, 'bo', markersize=3, transform=ccrs.PlateCarree(), label='Your location')
    if print_time == True:
        ax.plot([], [], 'gx', markersize=0, transform=ccrs.PlateCarree(), label= time_now)
    if print_elevation == True:
        ax.plot([], [], 'gx', markersize=0, transform=ccrs.PlateCarree(), label= f'now elevation is {str(sat_elev[mid])[0:7]} km')

    sector_lons = []
    sector_lats = []
    for i in range(1, len(sat_lons)-1):
        if np.abs(sat_lons[i] - sat_lons[i-1]) > 180:
            ax.plot(sector_lons, sector_lats, f'{color}-', linewidth=0.8, transform=ccrs.PlateCarree())
            sector_lons = []
            sector_lats = []
        else:
            sector_lons.append(sat_lons[i])
            sector_lats.append(sat_lats[i])


    plt.legend()
    plt.title(f'Orbit of {sat_name}', pad=5)
    
    plt.show()


def visualization_orbit_for_satellites(sats, time_now, end_hour, step, lons_obs, lats_obs, print_time = True, print_elevation = True):
    colors = ['r', 'y', 'g', 'b', 'm', 'c', 'k', 'orange', 'purple', 'pink']
    
    def binaary_searh_for_utc(utc, time):
        if time[:10] == utc[0][:10]:
            target_time = int(time[11:13]+ time[14:16])
            right, left = 0, len(utc) - 1
            mid = (right + left) // 2

            while right <= left:
                mid = (right + left) // 2
                check_time = int(utc[mid][11:13] + utc[mid][14:16])
                if check_time < target_time:
                    right = mid + 1
                else:
                    left = mid - 1
            return mid
        else:
            return "Расчеты орбит устарели"

    year, month, day = map(int, time_now.split()[0].split('-'))
    hour, minute, second = map(int, time_now.split()[1].split(':'))
    date = datetime.datetime(year, month, day, hour, minute, second) #cartopy работает только с datetime
    
    plt.figure(figsize=(12, 12))
    ax = plt.axes(projection=ccrs.PlateCarree())
    
    ax.add_feature(cfeature.COASTLINE, linewidth=0.5)
    ax.add_feature(Nightshade(date, alpha=0.3))
    ax.stock_img() 

    ax.gridlines(draw_labels=True, linewidth=0.5, color='gray', alpha=0.5, linestyle='--')
    ax.plot(lons_obs, lats_obs, 'bo', markersize=3, transform=ccrs.PlateCarree(), label='Your location')
    if print_time == True:
        ax.plot([], [], 'gx', markersize=0, transform=ccrs.PlateCarree(), label= time_now)

    for i in range(len(sats)):
        sat_name = sats[i]['name']
        sat_lons = sats[i]['longitudes']
        sat_lats = sats[i]['latitudes']
        sat_elev = sats[i]['elevations']
        time_utc = sats[i]['times in utc']

        mid = binaary_searh_for_utc(time_utc, time_now)
        sat_lons = sat_lons[mid: end_hour * step]
        sat_lats = sat_lats[mid: end_hour * step]

        ax.plot(sat_lons[0], sat_lats[0], f'{colors[i]}*', markersize=5, transform=ccrs.PlateCarree(), label=f'{sat_name}')
        #решение проблемы отрисовки горизонтальных линий
        sector_lons = []
        sector_lats = []
        for x in range(1, len(sat_lons)-1):
            if print_elevation == True:
                ax.plot([], [], f'{colors[i]}-', markersize=0, transform=ccrs.PlateCarree(), label= f'now elevation is {str(sat_elev[mid])[0:7]} km')
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
        framealpha=0.7             # Полупрозрачный фон
    )
    plt.title(f'Orbit of satellites', pad=5)
    
    plt.show()
