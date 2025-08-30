import numpy as np
import pyaudio
import rtlsdr
import wave

class SDR_recoder:
    def __init__(self, center_freq: int, sample_rate: int, threshold: float, 
                 duration: float, output_file: str):
        self.center_freq = center_freq
        self.sample_rate = sample_rate
        self.threshold = threshold
        self.duration = duration
        self.output_file = output_file
        