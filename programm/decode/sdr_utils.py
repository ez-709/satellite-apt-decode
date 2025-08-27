import numpy as np
import pyaudio
import rtlsdr
import wave

class FRSScanner:
    """
    Класс для сканирования частот FRS с использованием RTL-SDR устройства и записи в WAV-файл при обнаружении передачи.

    Атрибуты:
    - center_freq: int
        Центральная частота для сканирования частот FRS.
    - sample_rate: int
        Частота дискретизации для RTL-SDR устройства.
    - threshold: float
        Пороговое значение для определения наличия передачи.
    - duration: float
        Длительность в секундах для записи при обнаружении передачи.
    - output_file: str
        Путь к выходному WAV-файлу.
    """

    def __init__(self, center_freq: int, sample_rate: int, threshold: float, duration: float, output_file: str):
        """
        Конструктор класса FRSScanner.

        Параметры:
        - center_freq: int
            Центральная частота для сканирования частот FRS.
        - sample_rate: int
            Частота дискретизации для RTL-SDR устройства.
        - threshold: float
            Пороговое значение для определения наличия передачи.
        - duration: float
            Длительность в секундах для записи при обнаружении передачи.
        - output_file: str
            Путь к выходному WAV-файлу.
        """

        self.center_freq = center_freq
        self.sample_rate = sample_rate
        self.threshold = threshold
        self.duration = duration
        self.output_file = output_file

    def scan_and_record(self):
        """
        Сканирует частоты FRS с использованием RTL-SDR устройства и записывает в WAV-файл при обнаружении передачи.

        Выбрасывает:
        - ValueError:
            Ошибка будет выброшена, если длительность меньше или равна нулю.
        """

        # Проверка корректности длительности
        if self.duration <= 0:
            raise ValueError("Длительность должна быть больше нуля.")

        # Создание экземпляра RTL-SDR устройства
        sdr = rtlsdr.RtlSdr()

        try:
            # Установка центральной частоты и частоты дискретизации
            sdr.center_freq = self.center_freq
            sdr.sample_rate = self.sample_rate

            # Вычисление количества отсчётов для чтения на основе длительности
            num_samples = int(self.sample_rate * self.duration)

            # Создание пустого массива для хранения отсчётов
            samples = np.empty(num_samples, dtype=np.complex64)

            # Запуск асинхронного чтения отсчётов
            sdr.read_samples_async(samples, num_samples)

            # Создание экземпляра PyAudio для воспроизведения аудио
            audio = pyaudio.PyAudio()

            # Открытие WAV-файла для записи
            wav_file = wave.open(self.output_file, 'wb')

            # Установка параметров WAV-файла
            wav_file.setnchannels(1)  # Моно
            wav_file.setsampwidth(audio.get_sample_size(pyaudio.paFloat32))
            wav_file.setframerate(self.sample_rate)

            # Переменная для отслеживания количества записанных отсчётов
            num_recorded_samples = 0

            # Переменная для хранения времени начала передачи
            start_time = None

            # Переменная для отслеживания, идёт ли в данный момент запись передачи
            is_recording = False

            # Цикл до тех пор, пока не будет записано нужное количество отсчётов
            while num_recorded_samples < num_samples:
                # Чтение части отсчётов с RTL-SDR устройства
                sdr_samples = sdr.read_samples(1024)

                # Вычисление мощности отсчётов
                power = np.mean(np.abs(sdr_samples) ** 2)

                # Проверка, превышает ли мощность пороговое значение
                if power > self.threshold:
                    # Если передача ещё не записывается, начать запись
                    if not is_recording:
                        is_recording = True
                        start_time = num_recorded_samples / self.sample_rate

                    # Запись отсчётов в WAV-файл
                    wav_file.writeframes(sdr_samples.tobytes())

                # Если идёт запись передачи, проверить, достигнута ли заданная длительность
                if is_recording and num_recorded_samples / self.sample_rate - start_time >= self.duration:
                    is_recording = False

                # Увеличение счётчика записанных отсчётов
                num_recorded_samples += len(sdr_samples)

            # Закрытие WAV-файла
            wav_file.close()

        finally:
            # Остановка RTL-SDR устройства
            sdr.close()

            # Завершение работы PyAudio
            audio.terminate()

# Пример использования класса FRSScanner:

# Инициализация FRSScanner с нужными параметрами
scanner = FRSScanner(center_freq=462550000, sample_rate=2400000, threshold=0.01, duration=5, output_file="recording.wav")

# Сканирование и запись частот FRS
try:
    scanner.scan_and_record()
    print("Запись успешно завершена.")
except ValueError as e:
    print(f"Ошибка при сканировании и записи: {e}")