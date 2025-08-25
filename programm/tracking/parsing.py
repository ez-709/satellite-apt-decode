import requests
import time

def get_not_deb_tle(url, active_names):
    '''
    функция собирает данные по указанному url, отсекая космический мусор DEB
    возвращает список списков TLE исходя из тех активных спутников, что были заданы на входе в функцию
    '''

    headers = {
        'User-Agent': 'SatelliteTracker/1.0 (egor.zhuravlev0407@gmail.com)'
    }
    
    response = requests.get(url, headers=headers, timeout=30)
    
    if response.status_code == 200:
        tle_data = response.text
        
        lines = tle_data.split('\n')
        tles = []
        for i in range(0, len(lines) - 2, 3):
            if i + 2 >= len(lines):
                break
            if "DEB" in lines[i]:
                continue
            line1 = lines[i].strip()
            line2 = lines[i + 1].strip()
            line3 = lines[i + 2].strip()
            tles.append([line1, line2, line3])

        filtered_tles = []
        for tle in tles:
            sat_name = tle[0].strip()
            if sat_name in active_names:
                filtered_tles.append(tle)
        
        return filtered_tles
        
    elif response.status_code == 403:
        print(f"Доступ запрещен к {url}. Код 403")
        return response.status_code
    elif response.status_code == 429:
        print(f"Слишком много запросов к {url}. Код 429")
        return response.status_code
    else:
        print(f"Ошибка загрузки данных. Код ошибки: {response.status_code}")
        return response.status_code