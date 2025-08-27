from rtlsdr import RtlSdr
import numpy as np
import matplotlib.pyplot as plt

sdr = RtlSdr()
sdr.sample_rate = 2.048e6
sdr.center_freq = 100e6
sdr.gain = 49.6

fft_size = 512
num_rows = 2.084e6
x = sdr.read_samples(fft_size * num_rows) 

spectrogram = np.zeros((num_rows, fft_size))
for i in range(num_rows):
    spectrogram[i,:] = 10*np.log10(np.abs(np.fft.fftshift(np.fft.fft(x[i*fft_size:(i+1)*fft_size])))**2)


extent = [98.976, 101.024, 0.125, 0]
plt.imshow(spectrogram, aspect='auto', extent=extent)
plt.xlabel("Frequency [MHz]")
plt.ylabel("Time [s]")
plt.show()

sdr.close()