import requests

def get_not_deb_tle(url, active_names):
    '''
    функция собирает данные по указанному url, отсекая космический мусор DEB
    возвращает список списков TLE исходя из тех активных спутников, что были заданы на входе в функцию
    '''
    data = requests.get(url)
    if data.status_code == 200:
        tle_data = data.text
        
        lines = tle_data.split('\n')
        tles = []
        for i in range(0, len(lines) - 2, 3):
            if "DEB" in lines[i]:
                continue
            line1 = lines[i].strip()
            line2 = lines[i+ 1].strip()
            line3 = lines[i + 2].strip()
            tles.append([line1, line2, line3])

        for i in range(len(tles) - 1, -1, -1):
            tle = tles[i]
            sat_name = tle[0].strip()
            if sat_name not in active_names:
                del tles[i]

        return tles
    else:
        print(f"Ошибка загрузки данных. Код ошибки: {data.status_code}")
        return None