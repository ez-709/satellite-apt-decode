import os
import scipy.io.wavfile as wav
import scipy.signal
import numpy as np
import matplotlib.pyplot as plt
import time

def normalize(signal, plow=5, phigh=95):
    low, high = np.percentile(signal, (plow, phigh))
    data = np.round(255 * (signal - low) / (high - low))
    return np.clip(data, 0, 255).astype(np.uint8)

def make_lines(signal):
    syncA = np.array([0, 0, 255, 255, 0, 0, 255, 255,
                      0, 0, 255, 255, 0, 0, 255, 255,
                      0, 0, 255, 255, 0, 0, 255, 255,
                      0, 0, 255, 255, 0, 0, 0, 0, 0,
                      0, 0, 0]) - 128
    peaks = [(0, 0)]
    mindistance = 2000
    signalshifted = signal.astype(np.int16) - 128
    for i in range(len(signal)-len(syncA)):
        corr = np.dot(syncA, signalshifted[i : i+len(syncA)])
        if i - peaks[-1][0] > mindistance:
            peaks.append((i, corr))
        elif corr > peaks[-1][1]:
            peaks[-1] = (i, corr)
    matrix = []
    for i in range(len(peaks) - 1):
        row = signal[peaks[i][0] : peaks[i][0] + 2080]
        if len(row) == 2080:
            matrix.append(row)
    return np.array(matrix)

def decoder_apt(wav_path):
    start_time = time.time()
    fs, data = wav.read(wav_path)
    if data.ndim > 1:
        data = data[:, 0]
    coef = 20800 / fs
    samples = int(coef * len(data))
    data_resampled = scipy.signal.resample(data, samples)
    analytic_signal = np.abs(scipy.signal.hilbert(data_resampled))
    analytic_signal = scipy.signal.resample(analytic_signal, len(analytic_signal)//5)
    normalized_signal = normalize(analytic_signal)
    matrix = make_lines(normalized_signal)
    plt.imshow(matrix, cmap='gray', aspect='auto')
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(wav_path)
    plt.close()

