from rtlsdr import RtlSdr
import numpy as np
import wave
import time
import os

from storage import write_logs
from tracking.utils import unix_to_utc

def record_radio_wav(center_freq_hz, cd_record, record_time=15 * 60, gain='auto', bandwidth=2.048e6):
    cd = os.getcwd() 
    cd_logs_decode = os.path.join(cd, 'programm', 'data','logs', 'logs_tech.txt')

    sdr = RtlSdr()
    sdr.sample_rate = bandwidth 
    sdr.center_freq = center_freq_hz
    sdr.gain = gain
    slot_duration = 1
    slot_size = int(sdr.sample_rate * slot_duration)

    target_rate = 20800 

    write_logs(cd_logs_decode, f'Запись начата в {unix_to_utc(time.time())}')
    start_time = time.time()

    wav = wave.open(cd_record, 'wb')
    wav.setnchannels(1)  
    wav.setsampwidth(2)  
    wav.setframerate(target_rate) 

    try:
        for i in range(int(record_time / slot_duration)):
            samples = sdr.read_samples(slot_size)

            am_block = np.abs(samples).astype(np.float32)

            num_target_samples_block = int(len(am_block) * target_rate / sdr.sample_rate)
            
            if num_target_samples_block > 0:
                x_original_block = np.linspace(0, len(am_block), len(am_block), endpoint=False)
                x_target_block = np.linspace(0, len(am_block), num_target_samples_block, endpoint=False)
                apt_block_resampled = np.interp(x_target_block, x_original_block, am_block)

                if apt_block_resampled.size > 0:
                    max_val = np.max(np.abs(apt_block_resampled))
                    if max_val > 0:
                        apt_block_normalized = apt_block_resampled / max_val
                    else:
                        apt_block_normalized = apt_block_resampled # Е
                        
                    apt_block_int16 = np.int16(apt_block_normalized * 32767)

                    wav.writeframes(apt_block_int16.tobytes())
            else:
                write_logs(cd_logs_decode, f"Предупреждение: Пропущен блок {i+1} из-за нулевого размера после интерполяции.")

    except Exception as e:
        write_logs(cd_logs_decode, f"Ошибка при записи/чтении: {e}")
    finally:
        wav.close()
        sdr.close()

    write_logs(cd_logs_decode, f'Запись завершена в {unix_to_utc(time.time())}\n')
