import io
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from datetime import datetime
from skyfield.api import load
from cartopy.feature.nightshade import Nightshade

from .calculation import calculate_now_position, calculate_radius_and_coordinates_of_circle
from .utils import binary_search, find_next_passe, unix_to_utc, filter_by_names

def setup_map(time_now_utc):
    plt.figure(figsize=(12, 12))
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.add_feature(Nightshade(time_now_utc, alpha=0.3))
    ax.add_feature(cfeature.LAND)
    ax.add_feature(cfeature.OCEAN)
    ax.add_feature(cfeature.COASTLINE, linewidth=0.5)
    ax.add_feature(cfeature.BORDERS, linestyle=':', linewidth=0.5)
    ax.add_feature(cfeature.LAKES, alpha=0.5)
    ax.add_feature(cfeature.RIVERS, linewidth=0.5)
    ax.gridlines(draw_labels=True, linewidth=0.5, color='gray', alpha=0.5, linestyle='--')
    return plt.gcf(), ax

def plot_antenna_location(ax, lons_obs, lats_obs):
    ax.plot(lons_obs, lats_obs, 'o', color='black', markersize=3, transform=ccrs.PlateCarree(), label='Локация антенны')

def plot_satellite_visibility_zone(ax, lon, lat, altitude, color_):
    radius, circle_lons, circle_lats = calculate_radius_and_coordinates_of_circle(lon, lat, altitude)
    ax.plot(circle_lons, circle_lats, '-', color=color_, linewidth=0.8, transform=ccrs.PlateCarree())

def plot_satellite_now_position(ax, lon, lat, color_, sat_name):
    ax.plot(lon, lat, '*', color=color_, markersize=5, transform=ccrs.PlateCarree(), label=f'{sat_name}')

def plot_orbits_of_satellites(ax, sat_lons, sat_lats, color_):
    sector_lons = []
    sector_lats = []
    
    for x in range(len(sat_lons)):
        if x > 0 and abs(sat_lons[x] - sat_lons[x - 1]) > 180:
            ax.plot(sector_lons, sector_lats, '-', color=color_, linewidth=1, transform=ccrs.PlateCarree())
            sector_lons = []
            sector_lats = []
        else:
            sector_lons.append(sat_lons[x])
            sector_lats.append(sat_lats[x])
    
    if sector_lons:
        ax.plot(sector_lons, sector_lats, '-', color=color_, linewidth=1, transform=ccrs.PlateCarree())

def plot_satellites_orbits(sats, tles, time_now_unix, end_hour, step, ax, colors):
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

        if time_now_unix < time_unix[right]:
            sat_lons = sat_lons[right: right + end_hour * step]
            sat_lats = sat_lats[right: right + end_hour * step]
        else:
            sat_lons = [now_longitudes] + sat_lons[right+1: right + end_hour * step]
            sat_lats = [now_latitudes] + sat_lats[right+1: right + end_hour * step]

        plot_satellite_visibility_zone(ax, now_longitudes, now_latitudes, now_altitude, colors[i])
        plot_satellite_now_position(ax, now_longitudes, now_latitudes, colors[i], sat_name)
        plot_orbits_of_satellites(ax, sat_lons, sat_lats, colors[i])

def plot_legend(ax):
    ax.legend(
        loc='lower left',          # Якорь легенды в нижнем левом углу
        bbox_to_anchor=(0, 0),     # Фиксированное положение (x=0, y=0)
        fontsize='small',        # Уменьшенный шрифт
        markerscale=0.6,           # Уменьшение размера маркеров
        framealpha=0.6             # Полупрозрачный фон
    )

def plot_tittle(sats, end_hour, filter_of):
    if filter_of == True and len(sats) > 1:
        plt.title(f'Орбиты спутников на ближайшие {end_hour} часов, отфильтрованы по {", ".join(str(el) for el in filter_of)}', pad=5)
    elif len(sats) == 1:
        name = sats[0]['name']
        plt.title(f'Орбита спутника {name} на ближайшие {end_hour} часов', pad=5)
    else:
        plt.title(f'Орбиты спутников на ближайшие {end_hour} часов', pad=5)

def return_legend(time_now_unix,tles, passes, names):
    most_closest_sat_name_passe, most_closest_time_rise, most_closest_time_set, duration = find_next_passe(time_now_unix, passes, names)
    rise_str = unix_to_utc(most_closest_time_rise)
    set_str = unix_to_utc(most_closest_time_set)

    tles = filter_by_names(names, tles)
    
    minutes_duration, seconds_duration = [int(i) for i in duration.split(':')]

    text = f'Данные орбиты рассчитаны для времени: {unix_to_utc(time_now_unix)}\n\n'
    
    text += (
        f"Следующий пролёт у {most_closest_sat_name_passe}\n"
        f"Восход: {rise_str}\n"
        f"Заход: {set_str}\n"
        f"Длительность: {minutes_duration} мин {seconds_duration} сек\n\n"
    )

    text += f'Текущая высота спутников:\n'

    for tle in tles:
        now_longitudes, now_latitudes, now_altitude = calculate_now_position(tle)
        name = tle['name']
        text += f'{name} на высоте {str(now_altitude)[0:3]} км\n\n'

    text += 'Круги вокруг спутников - это зоны, где спутники сейчас над горизонтом.'

    return text

def visualization_orbit_for_satellites(sats, time_now_unix, end_hour, step, lons_obs, lats_obs, tles, filter_of):
    colors = ["#D40A0A", "#F1B501", "#007034", "#2800BA", '#A23B72', "#00DCBF", "#000000", "#803A0F", "#8C8C8C", "#691D3F", '#D68FD6']

    ts = load.timescale()
    time_now_utc = ts.now().utc_datetime()

    fig, ax = setup_map(time_now_utc)

    plot_antenna_location(ax, lons_obs, lats_obs)
    plot_satellites_orbits(sats, tles, time_now_unix, end_hour, step, ax, colors)

    plot_legend(ax)
    plot_tittle(sats, end_hour, filter_of)

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    plt.close()
    buffer.seek(0)
    
    from aiogram.types import BufferedInputFile
    return BufferedInputFile(buffer.getvalue(), filename="orbits.png")

def orbits_and_legend(sats_coors, time_now_unix, end_hour, step, lons_obs, lats_obs, names, tles, passes, filter_of):
    sat_coors = filter_by_names(names, sats_coors)
    graph = visualization_orbit_for_satellites(sat_coors, time_now_unix, end_hour, step, lons_obs, lats_obs, tles,filter_of)
    legend = return_legend(time_now_unix, tles, passes, names)
    return graph, legend
