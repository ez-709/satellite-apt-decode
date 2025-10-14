import time
from decode.decoding_procesing import record_and_decode_satellite, recors_sats_from_passes

def generate_passes(k, duration=2):
    """
    Генерирует k спутников, у каждого — по 2 прохождения.
    Общая продолжительность прохождения = duration секунд.
    """
    satellites = [
        "NOAA 15",
        "NOAA 18",
        "NOAA 19",
        "NOAA 20 (JPSS-1)",
        "NOAA 21 (JPSS-2)"
    ]
    
    passes = []
    start_time = time.time() + 5  # Через 5 секунд от запуска

    for i in range(k):
        sat_name = satellites[i % len(satellites)]  # Циклически выбираем спутник
        points = []
        current_time = start_time + i * 10  # Каждый спутник — с интервалом 10 секунд (2 пролёта по 5 сек)

        for j in range(2):  # Два пролёта на спутник
            rise = current_time + j * 5  # Каждые 5 секунд новый пролёт
            set_time = rise + duration
            culmination = (rise + set_time) / 2
            duration_formatted = f"{duration // 60}:{duration % 60:02d}"

            points.append({
                "rise": round(rise, 6),
                "culmination": f"{round(culmination, 6)} with 799.736 altitude and 45.0 degrees above horizon",
                "set": round(set_time, 6),
                "duration (min:sec)": duration_formatted
            })

        passes.append({
            "name": sat_name,
            "points": points
        })

    return passes

# Пример использования:
k = 3
result = generate_passes(k, duration=3)
import json
print(json.dumps(result, indent=2))
print('\n\n')

recors_sats_from_passes(result)