import os
import time
from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

import telegram_bot.keybords as kb 
from storage import json_to_py, find_satellites
from tracking.utils import (find_next_passes_for_satellites, find_next_passes_for_one_satellite)
from tracking.visualization import orbits_and_legend
from telegram_bot.bot_cashe import get_cached_data

cd = os.getcwd()
cd_sat = os.path.join(cd, 'programm', 'data', 'data_base', 'satellites.json')
cd_passes = os.path.join(cd, 'programm', 'data', 'data_base', 'passes.json')

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer('Меню', reply_markup=kb.menu)

back_handlers = {
    'Назад': ('Главное меню', kb.menu),
    'Назад к фильтрам пролетов': ('Выберите какие пролеты вас интересуют', kb.filter_passes),
    'Назад к группам пролетов': ('Выберите группу спутников', kb.group_passes),
    'Назад к частотам пролетов': ('Выберите частоту', kb.frequency_passes),
    'Назад к типам сигнала': ('Выберите тип сигнала', kb.type_signal_passes),
    'Назад к списку спутников': ('Выберите спутник', kb.names_passes),
    'Назад к орбитам': ('Выберите какие орбиты вас интересуют', kb.orbits),
    'Назад к группам орбит': ('Выберите группу спутников', kb.group_orbits),
    'Назад к частотам орбит': ('Выберите частоту', kb.frequency_orbits),
    'Назад к типам сигнала орбит': ('Выберите тип сигнала', kb.type_signal_orbits),
    'Назад к списку спутников орбит': ('Выберите спутник', kb.names_orbits),
    'Назад к фильтрам орбит': ('Орбиты спутников, отсортированные по:', kb.filter_orbits)
}

@router.message(F.text.in_(back_handlers.keys()))
async def back_handler(message: Message):
    text, keyboard = back_handlers[message.text]
    await message.answer(text, reply_markup=keyboard)

@router.message(F.text.in_(["Орбиты спутников", "Фотографии со спутников", "База спутников", "Пролеты спутников", "О проекте"]))
async def menu_handler(message: Message):
    if message.text == 'База спутников':
        satellites = json_to_py(cd_sat)
        text = ""
        for sat in satellites:
            text += f"*{sat['name']}*\n"
            text += f"NORAD ID: `{sat['norad id']}`\n"
            text += f"Частота: `{sat['frequency']} МГц`\n"
            text += f"Мин. время для записи сигнала: `{sat['min record time']}`\n"
            text += f"Тип сигнала: `{sat['signal type']}`\n"
            text += f"Группа: `{sat['group']}`\n\n"
        keyboard = kb.back
        parse_mode = "Markdown"
        
    elif message.text == 'О проекте':
        text = 'Проект автоматически рассчитывает орбиты спутников, визуализирует их на карте, обрабатывает и декодирует изображения, принимаемыми со спутников.'
        keyboard = kb.back
        parse_mode = None
        
    elif message.text == 'Пролеты спутников':
        text = 'Выберите какие пролеты вас интересуют'
        keyboard = kb.filter_passes
        parse_mode = None
        
    elif message.text == 'Орбиты спутников':
        text = 'Выберите какие орбиты вас интересуют'
        keyboard = kb.orbits
        parse_mode = None
        
    elif message.text == 'Фотографии со спутников':
        text = 'Фотографии спутников (в разработке)'
        keyboard = kb.back
        parse_mode = None
    
    await message.answer(text, parse_mode=parse_mode, reply_markup=keyboard)

filter_handlers = {
    'passes': {
        'Ближайшие пролеты каждого спутника': (None, 'Выберите какие пролеты вас интересуют', kb.back_to_filter_passes),
        'По частоте': ('frequency', 'Выберите частоту:', kb.frequency_passes),
        'По типу сигнала': ('signal_type', 'Выберите тип сигнала:', kb.type_signal_passes),
        'По группе': ('group', 'Выберите группу:', kb.group_passes),
        'Пролеты конкретного спутника': ('satellite', 'Введите название спутника для поиска пролетов:', kb.names_passes),
    },
    'orbits': {
        'По частоте': ('frequency', 'Выберите частоту:', kb.frequency_orbits),
        'По типу сигнала': ('signal_type', 'Выберите тип сигнала:', kb.type_signal_orbits),
        'По группе': ('group', 'Выберите группу:', kb.group_orbits),
        'Орбита конкретного спутника': ('satellite', 'Введите название спутника для поиска орбит:', kb.names_orbits),
    }
}

@router.message(F.text.in_(list(filter_handlers['passes'].keys()) + list(filter_handlers['orbits'].keys())))
async def handle_filters(message: Message):
    filter_type = 'passes' if message.text in filter_handlers['passes'] else 'orbits'
    config = filter_handlers[filter_type][message.text]
    
    if config[0] is None: 
        names, filter_of = find_satellites(cd_sat)
        next_passes = find_next_passes_for_satellites(json_to_py(cd_passes), names)
        text = "Ближайшие пролеты спутников:\n\n" + '\n\n'.join(next_passes)
        keyboard = config[2]
    else:
        text = config[1]
        keyboard = config[2]

    await message.answer(text, reply_markup=keyboard)

freq_config = {
    'passes': {
        '137 МГц': (137, kb.back_to_frequency_passes),
        '1.7 ГГц': (1698, kb.back_to_frequency_passes),
    },
    'orbits': {
        '137 МГц': (137, kb.freq_137_orbits), 
        '1.7 ГГц': (1698, kb.freq_1700_orbits),  
    }
}

@router.message(F.text.in_(list(freq_config['passes'].keys()) + list(freq_config['orbits'].keys())))
async def freq_handler(message: Message, step: int = None,
                              obs_lon: float = None, obs_lat: float = None):
    
    sats_coors, sats_tle, passes = get_cached_data()

    handler_type = 'passes' if message.text in freq_config['passes'] else 'orbits'
    frequency, keyboard = freq_config[handler_type][message.text]
    
    names, filter_of = find_satellites(cd_sat, frequency=frequency)
    
    if handler_type == 'passes':
        next_passes = find_next_passes_for_satellites(json_to_py(cd_passes), names)
        text = f"Ближайшие пролеты спутников, отсортированные по {filter_of[0]}:\n\n" + '\n\n'.join(next_passes)
        await message.answer(text, reply_markup=keyboard)
    else: 
        unix_time_now = time.time()
        buffer, text = orbits_and_legend(
            sats_coors=sats_coors,    
            time_now_unix=unix_time_now,
            end_hour=2,
            step=step,
            lons_obs=obs_lon,
            lats_obs=obs_lat,
            names=names,
            tles=sats_tle,
            passes=passes,
            filter_of=filter_of
        )
        await message.answer_photo(photo=buffer, caption=text, reply_markup=keyboard)

signal_config = {
    'passes': {
        'APT': ('APT', kb.back_to_signal_passes),
        'HRPT': ('HRPT', kb.back_to_signal_passes),
        'LRPT': ('LRPT', kb.back_to_signal_passes),
    },
    'orbits': {
        'APT': ('APT', kb.signal_APT_orbits),
        'HRPT': ('HRPT', kb.signal_HRPT_orbits),
        'LRPT': ('LRPT', kb.signal_LRPT_orbits),  
    }
}

@router.message(F.text.in_(list(signal_config['passes'].keys()) + list(signal_config['orbits'].keys())))
async def signal_handler(message: Message, step: int = None,
                              obs_lon: float = None, obs_lat: float = None):
    
    sats_coors, sats_tle, passes = get_cached_data()

    handler_type = 'passes' if message.text in signal_config['passes'] else 'orbits'
    signal_type, keyboard = signal_config[handler_type][message.text]
    
    names, filter_of = find_satellites(cd_sat, signal_type=signal_type)
    
    if handler_type == 'passes':
        next_passes = find_next_passes_for_satellites(json_to_py(cd_passes), names)
        text = f"Ближайшие пролеты спутников, отсортированные по {filter_of[0]}:\n\n" + '\n\n'.join(next_passes)
        await message.answer(text, reply_markup=keyboard)
    else:
        unix_time_now = time.time()
        buffer, text = orbits_and_legend(
            sats_coors=sats_coors,    
            time_now_unix=unix_time_now,
            end_hour=2,
            step=step,
            lons_obs=obs_lon,
            lats_obs=obs_lat,
            names=names,
            tles=sats_tle,
            passes=passes,
            filter_of=filter_of
        )
        await message.answer_photo(photo=buffer, caption=text, reply_markup=keyboard)

group_config = {
    'passes': {
        'NOAA': ('NOAA', kb.back_to_group_passes),
        'Meteor': ('Meteor', kb.back_to_group_passes),
    },
    'orbits': {
        'NOAA': ('NOAA', kb.group_NOAA_orbits),
        'Meteor': ('Meteor', kb.group_Meteor_orbits), 
    }
}

@router.message(F.text.in_(list(group_config['passes'].keys()) + list(group_config['orbits'].keys())))
async def group_handler(message: Message, step: int = None,
                              obs_lon: float = None, obs_lat: float = None):
    
    sats_coors, sats_tle, passes = get_cached_data()

    handler_type = 'passes' if message.text in group_config['passes'] else 'orbits'
    group_name, keyboard = group_config[handler_type][message.text]
    
    names, filter_of = find_satellites(cd_sat, group=group_name)
    
    if handler_type == 'passes':
        next_passes = find_next_passes_for_satellites(json_to_py(cd_passes), names)
        text = f"Ближайшие пролеты спутников, отсортированные по {filter_of[0]}:\n\n" + '\n\n'.join(next_passes)
        await message.answer(text, reply_markup=keyboard)
    else:
        unix_time_now = time.time()
        buffer, text = orbits_and_legend(
            sats_coors=sats_coors,    
            time_now_unix=unix_time_now,
            end_hour=2,
            step=step,
            lons_obs=obs_lon,
            lats_obs=obs_lat,
            names=names,
            tles=sats_tle,
            passes=passes,
            filter_of=filter_of
        )
        await message.answer_photo(photo=buffer, caption=text, reply_markup=keyboard)

satellite_config = {
    'passes': {
        'NOAA 15': ('NOAA 15', kb.back_to_names_passes),
        'NOAA 18': ('NOAA 18', kb.back_to_names_passes),
        'NOAA 19': ('NOAA 19', kb.back_to_names_passes),
        'NOAA 20 (JPSS-1)': ('NOAA 20 (JPSS-1)', kb.back_to_names_passes),
        'NOAA 21 (JPSS-2)': ('NOAA 21 (JPSS-2)', kb.back_to_names_passes),
        'METEOR-M 2': ('METEOR-M 2', kb.back_to_names_passes),
        'METEOR-M2 2': ('METEOR-M2 2', kb.back_to_names_passes),
    },
    'orbits': {
        'NOAA 15': ('NOAA 15', kb.NOAA_15_orbits),
        'NOAA 18': ('NOAA 18', kb.NOAA_18_orbits),
        'NOAA 19': ('NOAA 19', kb.NOAA_19_orbits),
        'NOAA 20 (JPSS-1)': ('NOAA 20 (JPSS-1)', kb.NOAA_20_orbits),
        'NOAA 21 (JPSS-2)': ('NOAA 21 (JPSS-2)', kb.NOAA_21_orbits),
        'METEOR-M 2': ('METEOR-M 2', kb.METEOR_M_2_orbits),
        'METEOR-M2 2': ('METEOR-M2 2', kb.METEOR_M2_2_orbits),
    }
}

@router.message(F.text.in_(list(satellite_config['passes'].keys()) + list(satellite_config['orbits'].keys())))
async def satellite_handler(message: Message, step: int = None,
                              obs_lon: float = None, obs_lat: float = None):
    
    sats_coors, sats_tle, passes = get_cached_data()

    handler_type = 'passes' if message.text in satellite_config['passes'] else 'orbits'
    satellite_name, keyboard = satellite_config[handler_type][message.text]
    
    if handler_type == 'passes':
        next_passes = find_next_passes_for_one_satellite(satellite_name, json_to_py(cd_passes))
        text = f"Ближайшие пролеты {satellite_name}:\n\n" + '\n\n'.join(next_passes)
        await message.answer(text, reply_markup=keyboard)
    else:
        names, filter_of = find_satellites(cd_sat, name=satellite_name)
        unix_time_now = time.time()
        buffer, text = orbits_and_legend(
            sats_coors=sats_coors,    
            time_now_unix=unix_time_now,
            end_hour=2,
            step=step,
            lons_obs=obs_lon,
            lats_obs=obs_lat,
            names=names,
            tles=sats_tle,
            passes=passes,
            filter_of=filter_of
        )
        await message.answer_photo(photo=buffer, caption=text, reply_markup=keyboard)

@router.message(F.text.in_({"Все спутники (2 часа)", "Орбиты спутников, отсортированные по:", "Орбита конкретного спутника"}))
async def orbits_handler(message: Message, step: int = None,
                              obs_lon: float = None, obs_lat: float = None):
    
    sats_coors, sats_tle, passes = get_cached_data()
    
    if message.text == 'Все спутники (2 часа)':
        names, filter_of = find_satellites(cd_sat)
        unix_time_now = time.time()
        buffer, text = orbits_and_legend(
            sats_coors=sats_coors,    
            time_now_unix=unix_time_now,
            end_hour=2,
            step=step,
            lons_obs=obs_lon,
            lats_obs=obs_lat,
            names=names,
            tles=sats_tle,
            passes=passes,
            filter_of=filter_of
        )
        await message.answer_photo(photo=buffer, caption=text, reply_markup=kb.all_orbit)
    
    elif message.text == 'Орбиты спутников, отсортированные по:':
        await message.answer("Орбиты спутников, отсортированные по:", reply_markup=kb.filter_orbits)
    
    elif message.text == "Орбита конкретного спутника":
        await message.answer("Выберите спутник:", reply_markup=kb.names_orbits)

@router.message(F.text == 'Обновить карту')
async def update_orbit_handler(message: Message, step: int = None,
                              obs_lon: float = None, obs_lat: float = None):
    
    sats_coors, sats_tle, passes = get_cached_data()
    
    names, filter_of = find_satellites(cd_sat)
    keyboard = kb.all_orbit
    
    unix_time_now = time.time()

    buffer, text = orbits_and_legend(
        sats_coors=sats_coors,    
        time_now_unix=unix_time_now,
        end_hour=2,
        step=step,
        lons_obs=obs_lon,
        lats_obs=obs_lat,
        names=names,
        tles=sats_tle,
        passes=passes,
        filter_of=filter_of
    )
    
    await message.answer_photo(photo=buffer, caption=text, reply_markup=keyboard)