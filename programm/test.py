from rtlsdr import RtlSdr

# Создание объекта SDR
sdr = RtlSdr()

# Настройка параметров (используй поддерживаемые значения)
sdr.sample_rate = 2.4e6  # 2.4 MHz - максимальная частота дискретизации
sdr.center_freq = 137.5e6  # Например, частота NOAA спутников
sdr.gain = 'auto'

print(f"Sample rate: {sdr.sample_rate} Hz")
print(f"Center frequency: {sdr.center_freq} Hz")
print(f"Gain: {sdr.gain}")

# Чтение данных
samples = sdr.read_samples(256*1024)
print(f"Read {len(samples)} samples")

# Закрытие устройства
sdr.close()