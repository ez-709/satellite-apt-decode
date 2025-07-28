from datetime import datetime, timedelta

time_now = '2025-07-28 18:00:18 UTC'
time_now = time_now[:19]
utc_date = datetime.strptime(time_now, '%Y-%m-%d %H:%M:%S')

end_time_hour = 48  
new_date = utc_date + timedelta(hours = end_time_hour)

new_date_string = new_date.strftime('%Y-%m-%d %H:%M:%S UTC')
print(new_date_string)