from rtlsdr import RtlSdr
import numpy as np
from scipy.io.wavfile import write

def record_radio_wav(center_freq_hz, cd_record, record_time=15 * 60, gain='auto', bandwidth=2.048e6):
    sdr = RtlSdr()
    sdr.sample_rate = bandwidth 
    sdr.center_freq = center_freq_hz
    sdr.gain = gain
    slot = int(sdr.sample_rate * 1)

    am_slots = []
    for i in range(record_time):
        samples = sdr.read_samples(slot)
        am_slots.append(np.abs(samples).astype(np.float32))

    sdr.close()
    am_signal = np.concatenate(am_slots)

    target_rate = 20800
    num_target_samples = int(len(am_signal) * target_rate / sdr.sample_rate)
    if num_target_samples > 0:
        x_original = np.linspace(0, len(am_signal), len(am_signal), endpoint=False)
        x_target = np.linspace(0, len(am_signal), num_target_samples, endpoint=False)
        apt_signal = np.interp(x_target, x_original, am_signal)
    else:
        apt_signal = np.array([], dtype=np.float32)

    if apt_signal.size > 0:
        apt_signal = apt_signal / np.max(np.abs(apt_signal))
        apt_signal_int16 = np.int16(apt_signal * 32767)
    else:
        apt_signal_int16 = np.array([], dtype=np.int16)

    write(cd_record, target_rate, apt_signal_int16)