from rtlsdr import RtlSdr

sdr = RtlSdr()

sdr.sample_rate = 2.4e6 
sdr.center_freq = 137.5e6  
sdr.gain = 'auto'





sdr.close()