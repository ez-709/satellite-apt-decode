import numpy as np
import matplotlib.pyplot as plt
import datetime

import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.feature.nightshade import Nightshade

def visualization_orbit_for_one_satellite(sat_coordinates, lons_obs, lats_obs, print_time = True, print_elevation = True, color = 'r'):
    sat_name, sat_lons, sat_lats, sat_elev, time = sat_coordinates

    year, month, day = map(int, time.split()[0].split('-'))
    hour, minute, second = map(int, time.split()[1].split(':'))
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
        ax.plot([], [], 'gx', markersize=0, transform=ccrs.PlateCarree(), label= time)
    if print_elevation == True:
        ax.plot([], [], 'gx', markersize=0, transform=ccrs.PlateCarree(), label= f'now elevation is {str(sat_elev[0])[0:7]} km')

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

