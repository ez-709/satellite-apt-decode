import time

from decode.decoding_procesing import record_and_decode_satellite
from tracking.utils import unix_to_utc

time_start = time.time()
print(unix_to_utc(time_start))
record_and_decode_satellite('NOAA 18', 12 * 60)
time_finish = time.time()
print('\n')
print(unix_to_utc(time_finish))
print('\n')
print(time_finish - time_start)

