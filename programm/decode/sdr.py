import numpy as np
import rtlsdr
import wave

def record_sdr(center_freq, sample_rate, duration, cd_output_file):
    sdr = rtlsdr.RtlSdr()

    sdr.center_freq = center_freq
    sdr.sample_rate = sample_rate
    num_samples = int(sample_rate * duration)

    samples = sdr.read_samples(num_samples)

    wav_file = wave.open(cd_output_file, 'wb')
    wav_file.setnchannels(2)  
    wav_file.setsampwidth(4) 
    wav_file.setframerate(sample_rate)


    audio_data = np.empty(2 * len(samples), dtype=np.float32)
    audio_data[0::2] = np.real(samples)  
    audio_data[1::2] = np.imag(samples)  
    sdr.close()