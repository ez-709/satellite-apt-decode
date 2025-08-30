from rtlsdr import RtlSdr
import numpy as np
import matplotlib.pyplot as plt

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

sdr.close()