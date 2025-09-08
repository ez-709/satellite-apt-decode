from rtlsdr import RtlSdr
import numpy as np
import matplotlib.pyplot as plt
import time

from skyfield.api import load
import os

from storage import json_to_py, read_config, add_rtl_sdr_libs_to_venv, clear_all_logs, find_satellites
from tracking.calculation import calculate_samples_from_hours
from background import background_calculations, background_update_tles
from tracking.visualization import orbits_and_legend

ts = load.timescale()
unix_time_now = ts.now().utc_datetime().timestamp()

cd = os.getcwd() 
cd_sat = os.path.join(cd, 'programm', 'data', 'data_base', 'satellites.json')
cd_tle = os.path.join(cd, 'programm', 'data', 'data_base', 'tle.json')
cd_processing = os.path.join(cd, 'programm', 'data', 'data_base', 'processing.json')
cd_coordinates = os.path.join(cd, 'programm', 'data', 'data_base', 'coordinates.json')
cd_passes = os.path.join(cd, 'programm', 'data', 'data_base', 'passes.json')
cd_config = os.path.join(cd, 'programm', 'config.json')
cd_decode = os.path.join(cd, 'programm', 'data_decode')
cd_logs_htpp = os.path.join(cd, 'programm', 'data','logs', 'logs_htpp.txt')
cd_logs_tech = os.path.join(cd, 'programm', 'data','logs', 'logs_tech.txt')
cd_logs_back = os.path.join(cd, 'programm', 'data','logs', 'logs_back.txt')

clear_all_logs(cd_logs_back, cd_logs_htpp, cd_logs_tech)


obs_lon, obs_lat, obs_alt, time_zone, step, end_time_hours, token, venv_name = read_config(cd_config)
cd_venv = os.path.join(cd, venv_name)
add_rtl_sdr_libs_to_venv(cd, cd_venv)
samples, step = calculate_samples_from_hours(end_time_hours)
tles = json_to_py(cd_tle)
sats_coor = json_to_py(cd_coordinates)
passes = json_to_py(cd_passes)

last_time = background_calculations(obs_lon, obs_lat, obs_alt, end_time_hours)


sats_coors = json_to_py(cd_coordinates)
names, filter_of = find_satellites(cd_sat)

buffer, text = orbits_and_legend(
            sats_coors=sats_coors,    
            time_now_unix=time.time(),
            end_hour=2,
            step=step,
            lons_obs=obs_lon,
            lats_obs=obs_lat,
            names=names,
            tles=tles,
            passes=passes,
            filter_of=filter_of
        )

    

'''
sdr = RtlSdr()
sdr.sample_rate = 2.048e6  
sdr.center_freq = 100e6  
sdr.gain = 20

fft_size = 512
record_time_seconds = 5

num_samples = int(sdr.sample_rate * record_time_seconds)
num_rows = num_samples // fft_size


x = sdr.read_samples(fft_size * num_rows) 

spectrogram = np.zeros((num_rows, fft_size))
for i in range(num_rows):
    spectrogram[i,:] = 10*np.log10(np.abs(np.fft.fftshift(np.fft.fft(x[i*fft_size:(i+1)*fft_size])))**2)

extent = [sdr.center_freq/1e6 - sdr.sample_rate/2/1e6, 
          sdr.center_freq/1e6 + sdr.sample_rate/2/1e6, 
          record_time_seconds, 0]

plt.imshow(spectrogram, aspect='auto', extent=extent)
plt.xlabel("Frequency [MHz]")
plt.ylabel("Time [s]")
plt.show()

sdr.close()'''