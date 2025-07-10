import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

#from parsing import get_not_deb_tle
from calculation import calculate_orbit

tles = [
    ['NOAA 15                 \r', '1 25338U 98030A   25190.96204984  .00000165  00000+0  85424-4 0  9998\r', '2 25338  98.5338 215.3601 0008990 270.3446  89.6705 14.26994218412489\r'], 
    ['NOAA 18                 \r', '1 28654U 05018A   25190.91599198  .00000059  00000+0  54361-4 0  9993\r', '2 28654  98.8422 270.0511 0014959  47.0049 313.2375 14.13617618 37954\r'], 
    ['NOAA 19                 \r', '1 33591U 09005A   25190.85655587  .00000135  00000+0  95974-4 0  9997\r', '2 33591  98.9962 255.7293 0012675 278.6650  81.3085 14.13387062846383\r'], 
    ['NOAA 20 (JPSS-1)        \r', '1 43013U 17073A   25190.86615621  .00000033  00000+0  36296-4 0  9996\r', '2 43013  98.7409 129.0539 0001315 131.0169 229.1121 14.19544169395908\r'], 
    ['NOAA 21 (JPSS-2)        \r', '1 54234U 22150A   25190.83163890  .00000013 00000+0  26681-4 0  9993\r', '2 54234  98.7274 129.2685 0002747  86.2765 273.8725 14.19543160137979\r']
]

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

def visualization(lons, lats):

    plt.figure(figsize=(12, 8))
    ax = plt.axes(projection=ccrs.PlateCarree())
    
    ax.add_feature(cfeature.COASTLINE, linewidth=0.5)
    ax.stock_img() 

    ax.gridlines(draw_labels=True, linewidth=0.5, color='gray', alpha=0.5, linestyle='--')
    ax.plot(lons, lats, 'r-', linewidth=0.8, transform=ccrs.PlateCarree())
    ax.plot(lons[0], lats[0], 'bx', markersize=10, transform=ccrs.PlateCarree(), label='Now')

    plt.legend()
    plt.title(f'Проекция орбиты спутника ', pad=5)
    plt.show()



longtitude, latitude, elevation = calculate_orbit(tles[1], 2.4, 4000)
visualization(longtitude, latitude)


