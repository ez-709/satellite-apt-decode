import requests

url = "https://celestrak.org/NORAD/elements/gp.php?NAME=NOAA&FORMAT=TLE"
noaa_active_names = ['NOAA 15', 'NOAA 18', 'NOAA 19', 'NOAA 20', 'NOAA 21']

#дописать код на случай если тле начинается с первой или второй строки
def get_not_deb_tle(url, active_names):
    '''
    фугкция собирает данные по указанному url, отсекая космический мусор DEB
    возвращает список списков TLE исходя из тех активных спутников, что были заданы на входе в функцию
    '''
    data = requests.get(url)
    if data.status_code == 200:
        tle_data = data.text
        
        lines = tle_data.split('\n')
        tles = []
        if lines[0][0] != 1 or lines[0][0] != 2:
            for index_line in range(0, len(lines) - 2, 3):
                if "DEB" in lines[index_line]:
                    continue
                else:
                    tles.append([lines[index_line], lines[index_line + 1], lines[index_line + 2]])

            for i in range(len(tles) - 1, -1, -1):
                tle = tles[i]
                if tle[0][:7] not in active_names:
                    tles.pop(i)

            return tles

    else:
        return f"Ошибка загрузки данных. Код ошибки: {data.status_code}"
    
print(get_not_deb_tle(url, noaa_active_names))