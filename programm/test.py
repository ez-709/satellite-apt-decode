from datetime import datetime

def calculate_delta_time_utc(time_1, time_2):
    '''
    фукнция считает 
    '''
    time_1 = datetime.strptime(time_1[:19], "%Y-%m-%d %H:%M:%S")
    time_1_unix = int(time_1.timestamp())
    time_2 = datetime.strptime(time_2[:19],  "%Y-%m-%d %H:%M:%S")
    time_2_unix = int(time_2.timestamp())
    return time_2_unix - time_1_unix

print(calculate_delta_time_utc("2025-07-24 08:41:39 UTC", "2025-07-24 08:41:49 UTC"))