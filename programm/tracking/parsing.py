import requests
import time
import random

from tracking.utils import unix_to_utc
from storage import *

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
        print(f"Доступ запрещен к {url}. Код 403\n")
        return response.status_code
    elif response.status_code == 429:
        print(f"Слишком много запросов к {url}. Код 429\n")
        return response.status_code
    else:
        print(f"Ошибка загрузки данных. Код ошибки: {response.status_code}\n")
        return response.status_code

def process_urls(cd_sat, cd_tle, cd_logs_htpp):
        tles = []
        urls = create_urls_to_htpp(cd_sat)
        for i, url in enumerate(urls):
            try:
                if i > 0:
                    time.sleep(random.uniform(1, 3))

                new_tles = get_not_deb_tle(url, active_names(cd_sat))
                if new_tles == 429:
                    write_logs(cd_logs_htpp, f'429 - слишком много запросов для {url} в {unix_to_utc(time.time())}\n')
                    time.sleep(60 * 60)

                elif new_tles == 403:
                    write_logs(cd_logs_htpp, f'403 - доступ запрещен для {url} в {unix_to_utc(time.time())}\n')
                    break

                elif isinstance(new_tles, int) and new_tles >= 400:
                    write_logs(cd_logs_htpp, f'HTTP ошибка {new_tles} для {url} в {unix_to_utc(time.time())}\n')
                    continue

                elif new_tles:
                    tles.append(new_tles)
                    write_logs(cd_logs_htpp, f"Успешно получено {len(new_tles)} TLE из {url} в {unix_to_utc(time.time())}\n")

            except Exception as e:
                write_logs(cd_logs_htpp, f"Неожиданная ошибка для {url}: {e} в {unix_to_utc(time.time())}\n")
                time.sleep(600)
                continue

        if tles:
            for tle_group in tles:
                write_or_update_tles(tle_group, cd_tle)
            write_logs(cd_logs_htpp, f"Обновлено TLE для {sum(len(t) for t in tles)} спутников в {unix_to_utc(time.time())}\n")