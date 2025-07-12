from tracking.parsing import get_not_deb_tle
from tracking.calculation import calculate_orbit
from tracking.visualization import visualization_orbit_for_one_satellite

url_noaa = "https://celestrak.org/NORAD/elements/gp.php?NAME=NOAA&FORMAT=TLE"
#url_meteor = "https://celestrak.org/NORAD/elements/gp.php?NAME=NOAA&FORMAT=TLE"
#url_iss = "https://celestrak.org/NORAD/elements/gp.php?NAME=NOAA&FORMAT=TLE"
noaa_active_names = ['NOAA 15', 'NOAA 18', 'NOAA 19', 'NOAA 20', 'NOAA 21']

tles = get_not_deb_tle(url_noaa, noaa_active_names)

"""tles = [
    ['NOAA 15', '1 25338U 98030A   25192.50463084  .00000165  00000+0  85569-4 0  9998', '2 25338  98.5338 216.8655 0008997 265.1501  94.8653 14.26994957412957'],
    ['NOAA 18', '1 28654U 05018A   25192.47314934  .00000051  00000+0  50383-4 0  9991', '2 28654  98.8422 271.5906 0014877  42.7816 317.4511 14.13617971 38255'],
    ['NOAA 19', '1 33591U 09005A   25192.41396440  .00000145  00000+0  10138-3 0  9990', '2 33591  98.9961 257.2952 0012671 273.8547  86.1176 14.13387759846601'],
    ['NOAA 20 (JPSS-1)', '1 43013U 17073A   25192.48730641  .00000027  00000+0  33532-4 0  9999', '2 43013  98.7410 130.6541 0001302 129.6058 230.5233 14.19544787396139'],
    ['NOAA 21 (JPSS-2)', '1 54234U 22150A   25191.74794225  .00000018  00000+0  29250-4 0  9996', '2 54234  98.7274 130.1716 0002751  84.6320 275.5170 14.19543300138104']
]
"""

print(tles)
sat_inf = calculate_orbit(tles[0], 4, 4000)
visualization_orbit_for_one_satellite(sat_inf, 37.6155600, 55.7522200, print_time = False)
