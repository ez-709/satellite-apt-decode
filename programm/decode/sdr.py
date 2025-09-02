import numpy as np
import rtlsdr
import wave

def record_sdr(center_freq, sample_rate, duration, output_file):
    sdr = rtlsdr.RtlSdr()

    sdr.center_freq = center_freq  
    sdr.sample_rate = sample_rate  
    sdr.gain = 'auto'
    
    print(f"Начинаю запись {duration} секунд на частоте {center_freq/1e6} МГц...")
    
    num_samples = int(sample_rate * duration)
    
    samples = sdr.read_samples(num_samples)
    sdr.close()
    
    i_data = np.real(samples) * 32767
    q_data = np.imag(samples) * 32767
    
    iq_data = np.empty(2 * len(samples), dtype=np.int16)
    iq_data[0::2] = i_data.astype(np.int16)
    iq_data[1::2] = q_data.astype(np.int16)
    
    with wave.open(output_file, 'wb') as wav_file:
        wav_file.setnchannels(2)  
        wav_file.setsampwidth(2)  
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(iq_data.tobytes())
    