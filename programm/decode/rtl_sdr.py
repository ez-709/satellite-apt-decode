from rtlsdr import RtlSdr
import numpy as np
from scipy.io.wavfile import write
from scipy.signal import resample

def record_radio_wav(center_freq_hz, cd_record, record_time = 15 * 60, gain = 'auto', bandwidth=2.048e6):
    sdr = RtlSdr()
    sdr.sample_rate = bandwidth 
    sdr.center_freq = center_freq_hz
    sdr.gain = gain

    num_samples = int(sdr.sample_rate * record_time)
    samples = sdr.read_samples(num_samples)
    sdr.close()

    am_signal = np.abs(samples)

    target_rate = 20800
    num_target_samples = int(len(am_signal) * target_rate / sdr.sample_rate)
    apt_signal = resample(am_signal, num_target_samples)

    apt_signal = apt_signal / np.max(np.abs(apt_signal))
    apt_signal_int16 = np.int16(apt_signal * 32767)

    write(cd_record, target_rate, apt_signal_int16)