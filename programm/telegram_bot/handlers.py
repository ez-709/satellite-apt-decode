import os
import time
from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

import telegram_bot.keybords as kb 
from telegram_bot.bot_cashe import get_cached_data
from tracking.parsing import process_urls
from storage import json_to_py, find_satellites
from tracking.utils import (find_next_passes_for_satellites, find_next_passes_for_one_satellite)
from tracking.visualization import orbits_and_legend
from background import make_all_calculations_ones

cd = os.getcwd() 
cd_sat = os.path.join(cd, 'programm', 'data', 'data_base', 'satellites.json')
cd_tle = os.path.join(cd, 'programm', 'data', 'data_base', 'tle.json')
cd_processing = os.path.join(cd, 'programm', 'data', 'data_base', 'processing.json')
cd_coordinates = os.path.join(cd, 'programm', 'data', 'data_base', 'coordinates.json')
cd_passes = os.path.join(cd, 'programm', 'data', 'data_base', 'passes.json')
cd_config = os.path.join(cd, 'programm', 'config.json')
cd_decode = os.path.join(cd, 'programm', 'data_decode')
cd_logs_htpp = os.path.join(cd, 'programm', 'data','logs', 'logs_htpp.txt')
cd_logs_tech = os.path.join(cd, 'programm', 'data','logs', 'logs_tech.txt')
cd_logs_back = os.path.join(cd, 'programm', 'data','logs', 'logs_back.txt')
cd_logs_decode = os.path.join(cd, 'programm', 'data','logs', 'logs_tech.txt')

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer('Меню', reply_markup=kb.menu)

back_handlers = {
    'back': ('Главное меню', kb.menu),
    'back_to_filter_passes': ('Выберите какие пролеты вас интересуют', kb.filter_passes),
    'back_to_group_passes': ('Выберите группу спутников', kb.group_passes),
    'back_to_frequency_passes': ('Выберите частоту', kb.frequency_passes),
    'back_to_signal_passes': ('Выберите тип сигнала', kb.type_signal_passes),
    'back_to_names_passes': ('Выберите спутник', kb.names_passes),
    'back_to_orbits': ('Выберите какие орбиты вас интересуют', kb.orbits),
    'back_to_group_orbits': ('Выберите группу спутников', kb.group_orbits),
    'back_to_frequency_orbits': ('Выберите частоту', kb.frequency_orbits),
    'back_to_signal_orbits': ('Выберите тип сигнала', kb.type_signal_orbits),
    'back_to_names_orbits': ('Выберите спутник', kb.names_orbits),
    'back_to_orbits_filter': ('Орбиты спутников, отсортированные по:', kb.filter_orbits),
    'back_to_secret_menu' : ('Выберите действие:', kb.secret_menu)
}

@router.callback_query(F.data.in_(back_handlers.keys()))
async def back_handler(callback: CallbackQuery):
    text, keyboard = back_handlers[callback.data]
    await callback.message.answer(text, reply_markup=keyboard)
    await callback.message.delete()
    await callback.answer()

@router.callback_query(F.data.in_(["satellites_base", "about", 'orbits', 'passes', 'photos']))
async def menu_handler(callback: CallbackQuery):
    if callback.data == 'satellites_base':
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
        
    elif callback.data == 'about':
        text = 'Проект автоматически рассчитывает орбиты спутников, визуализирует их на карте, обрабатывает и декодирует изображения, принимаемыми со спутников.'
        keyboard = kb.back
        parse_mode = None
        
    elif callback.data == 'passes':
        text = 'Выберите какие пролеты вас интересуют'
        keyboard = kb.filter_passes
        parse_mode = None
        
    elif callback.data == 'orbits':
        text = 'Выберите какие орбиты вас интересуют'
        keyboard = kb.orbits
        parse_mode = None
        
    elif callback.data == 'photos':
        text = 'Фотографии спутников (в разработке)'
        keyboard = kb.back
        parse_mode = None
    
    await callback.message.delete()
    await callback.message.answer(text, parse_mode=parse_mode, reply_markup=keyboard)
    await callback.answer()

filter_handlers = {
    'passes': {
        'filter_names_passes': (None, 'Выберите какие пролеты вас интересуют', kb.back_to_filter_passes),
        'filter_frequency_passes': ('frequency', 'Выберите частоту:', kb.frequency_passes),
        'filter_signal_type_passes': ('signal_type', 'Выберите тип сигнала:', kb.type_signal_passes),
        'filter_group_passes': ('group', 'Выберите группу:', kb.group_passes),
        'satellite_passes': ('satellite', 'Введите название спутника для поиска пролетов:', kb.names_passes),
    },
    'orbits': {
        'filter_frequency_orbits': ('frequency', 'Выберите частоту:', kb.frequency_orbits),
        'filter_signal_type_orbits': ('signal_type', 'Выберите тип сигнала:', kb.type_signal_orbits),
        'filter_group_orbits': ('group', 'Выберите группу:', kb.group_orbits),
        'satellite_orbits': ('satellite', 'Введите название спутника для поиска орбит:', kb.names_orbits),
    }
}

@router.callback_query(F.data.in_(list(filter_handlers['passes'].keys()) + list(filter_handlers['orbits'].keys())))
async def handle_filters(callback: CallbackQuery):
    filter_type = 'passes' if 'passes' in callback.data else 'orbits'
    config = filter_handlers[filter_type][callback.data]
    
    if config[0] is None: 
        names, filter_of = find_satellites(cd_sat)
        next_passes = find_next_passes_for_satellites(json_to_py(cd_passes), names)
        text = "Ближайшие пролеты спутников:\n\n" + '\n\n'.join(next_passes)
        keyboard = config[2]
    else:
        text = config[1]
        keyboard = config[2]
    
    await callback.message.delete()
    await callback.message.answer(text, reply_markup=keyboard)
    await callback.answer()

freq_config = {
    'passes': {
        'freq_137_passes': (137, kb.back_to_frequency_passes),
        'freq_1700_passes': (1698, kb.back_to_frequency_passes),
    },
    'orbits': {
        'freq_137_orbits': (137, kb.freq_137_orbits), 
        'freq_1700_orbits': (1698, kb.freq_1700_orbits),  
    }
}

@router.callback_query(F.data.in_(list(freq_config['passes'].keys()) + list(freq_config['orbits'].keys())))
async def freq_handler(callback: CallbackQuery, step: int = None,
                              obs_lon: float = None, obs_lat: float = None):
    
    sats_coors, sats_tle, passes = get_cached_data()

    handler_type = 'passes' if 'passes' in callback.data else 'orbits'
    frequency, keyboard = freq_config[handler_type][callback.data]
    
    names, filter_of = find_satellites(cd_sat, frequency=frequency)
    
    if handler_type == 'passes':
        next_passes = find_next_passes_for_satellites(json_to_py(cd_passes), names)
        text = f"Ближайшие пролеты спутников, отсортированные по {filter_of[0]}:\n\n" + '\n\n'.join(next_passes)
        await callback.message.delete()
        await callback.message.answer(text, reply_markup=keyboard)
    else:
        await callback.answer("Идет загрузка, подождите...")
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
        await callback.message.delete()
        await callback.message.answer_photo(photo=buffer, caption=text, reply_markup=keyboard)
    
    await callback.answer()

signal_config = {
    'passes': {
        'signal_APT_passes': ('APT', kb.back_to_signal_passes),
        'signal_HRPT_passes': ('HRPT', kb.back_to_signal_passes),
        'signal_LRPT_passes': ('LRPT', kb.back_to_signal_passes),
    },
    'orbits': {
        'signal_APT_orbits': ('APT', kb.signal_APT_orbits),
        'signal_HRPT_orbits': ('HRPT', kb.signal_HRPT_orbits),
        'signal_LRPT_orbits': ('LRPT', kb.signal_LRPT_orbits),  
    }
}

@router.callback_query(F.data.in_(list(signal_config['passes'].keys()) + list(signal_config['orbits'].keys())))
async def signal_handler(callback: CallbackQuery, step: int = None,
                              obs_lon: float = None, obs_lat: float = None):
    
    sats_coors, sats_tle, passes = get_cached_data()

    handler_type = 'passes' if 'passes' in callback.data else 'orbits'
    signal_type, keyboard = signal_config[handler_type][callback.data]
    
    names, filter_of = find_satellites(cd_sat, signal_type=signal_type)
    
    if handler_type == 'passes':
        next_passes = find_next_passes_for_satellites(json_to_py(cd_passes), names)
        text = f"Ближайшие пролеты спутников, отсортированные по {filter_of[0]}:\n\n" + '\n\n'.join(next_passes)
        await callback.message.delete()
        await callback.message.answer(text, reply_markup=keyboard)
    else:
        await callback.answer("Идет загрузка, подождите...")
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
        await callback.message.delete()
        await callback.message.answer_photo(photo=buffer, caption=text, reply_markup=keyboard)
    
    await callback.answer()

group_config = {
    'passes': {
        'group_NOAA_passes': ('NOAA', kb.back_to_group_passes),
        'group_Meteor_passes': ('Meteor', kb.back_to_group_passes),
    },
    'orbits': {
        'group_NOAA_orbits': ('NOAA', kb.group_NOAA_orbits),
        'group_Meteor_orbits': ('Meteor', kb.group_Meteor_orbits), 
    }
}

@router.callback_query(F.data.in_(list(group_config['passes'].keys()) + list(group_config['orbits'].keys())))
async def group_handler(callback: CallbackQuery, step: int = None,
                              obs_lon: float = None, obs_lat: float = None):
    
    sats_coors, sats_tle, passes = get_cached_data()

    handler_type = 'passes' if 'passes' in callback.data else 'orbits'
    group_name, keyboard = group_config[handler_type][callback.data]
    
    names, filter_of = find_satellites(cd_sat, group=group_name)
    
    if handler_type == 'passes':
        next_passes = find_next_passes_for_satellites(json_to_py(cd_passes), names)
        text = f"Ближайшие пролеты спутников, отсортированные по {filter_of[0]}:\n\n" + '\n\n'.join(next_passes)
        await callback.message.delete()
        await callback.message.answer(text, reply_markup=keyboard)
    else:
        await callback.answer("Идет загрузка, подождите...")
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
        await callback.message.delete()
        await callback.message.answer_photo(photo=buffer, caption=text, reply_markup=keyboard)
    
    await callback.answer()

satellite_config = {
    'passes': {
        'NOAA 15_passes': ('NOAA 15', kb.back_to_names_passes),
        'NOAA 18_passes': ('NOAA 18', kb.back_to_names_passes),
        'NOAA 19_passes': ('NOAA 19', kb.back_to_names_passes),
        'NOAA 20 (JPSS-1)_passes': ('NOAA 20 (JPSS-1)', kb.back_to_names_passes),
        'NOAA 21 (JPSS-2)_passes': ('NOAA 21 (JPSS-2)', kb.back_to_names_passes),
        'METEOR-M 2_passes': ('METEOR-M 2', kb.back_to_names_passes),
        'METEOR-M2 2_passes': ('METEOR-M2 2', kb.back_to_names_passes),
    },
    'orbits': {
        'NOAA 15_orbits': ('NOAA 15', kb.NOAA_15_orbits),
        'NOAA 18_orbits': ('NOAA 18', kb.NOAA_18_orbits),
        'NOAA 19_orbits': ('NOAA 19', kb.NOAA_19_orbits),
        'NOAA 20 (JPSS-1)_orbits': ('NOAA 20 (JPSS-1)', kb.NOAA_20_orbits),
        'NOAA 21 (JPSS-2)_orbits': ('NOAA 21 (JPSS-2)', kb.NOAA_21_orbits),
        'METEOR-M 2_orbits': ('METEOR-M 2', kb.METEOR_M_2_orbits),
        'METEOR-M2 2_orbits': ('METEOR-M2 2', kb.METEOR_M2_2_orbits),
    }
}

@router.callback_query(F.data.in_(list(satellite_config['passes'].keys()) + list(satellite_config['orbits'].keys())))
async def satellite_handler(callback: CallbackQuery, step: int = None,
                              obs_lon: float = None, obs_lat: float = None):
    
    sats_coors, sats_tle, passes = get_cached_data()

    handler_type = 'passes' if 'passes' in callback.data else 'orbits'
    satellite_name, keyboard = satellite_config[handler_type][callback.data]
    
    if handler_type == 'passes':
        next_passes = find_next_passes_for_one_satellite(satellite_name, json_to_py(cd_passes))
        text = f"Ближайшие пролеты {satellite_name}:\n\n" + '\n\n'.join(next_passes)
        await callback.message.delete()
        await callback.message.answer(text, reply_markup=keyboard)
    else:
        await callback.answer("Идет загрузка, подождите...")
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
        await callback.message.delete()
        await callback.message.answer_photo(photo=buffer, caption=text, reply_markup=keyboard)
    
    await callback.answer()

@router.callback_query(F.data.in_({"orbits_all_2h", "orbits_by_filter", "orbits_one_satellite"}))
async def orbits_handler(callback: CallbackQuery, step: int = None,
                              obs_lon: float = None, obs_lat: float = None):
    
    sats_coors, sats_tle, passes = get_cached_data()
    
    if callback.data == 'orbits_all_2h':
        await callback.answer("Идет загрузка, подождите...")
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
        await callback.message.delete()
        await callback.message.answer_photo(photo=buffer, caption=text, reply_markup=kb.all_orbit)
    
    elif callback.data == 'orbits_by_filter':
        await callback.message.delete()
        await callback.message.answer("Орбиты спутников, отсортированные по:", reply_markup=kb.filter_orbits)
    
    elif callback.data == "orbits_one_satellite":
        await callback.message.delete()
        await callback.message.answer("Выберите спутник:", reply_markup=kb.names_orbits)
    
    await callback.answer()

@router.callback_query(F.data.startswith('update_'))
async def update_orbit_handler(callback: CallbackQuery, step: int = None,
                              obs_lon: float = None, obs_lat: float = None):
    
    sats_coors, sats_tle, passes = get_cached_data()
    
    update_type = callback.data
    
    unix_time_now = time.time()

    await callback.answer("Идет загрузка, подождите...")

    if update_type == 'update_orbit_all':
        names, filter_of = find_satellites(cd_sat)
        keyboard = kb.all_orbit
    elif update_type == 'update_freq_137':
        names, filter_of = find_satellites(cd_sat, frequency=137)
        keyboard = kb.freq_137_orbits
    elif update_type == 'update_freq_1700':
        names, filter_of = find_satellites(cd_sat, frequency=1698)
        keyboard = kb.freq_1700_orbits
    elif update_type == 'update_signal_APT':
        names, filter_of = find_satellites(cd_sat, signal_type='APT')
        keyboard = kb.signal_APT_orbits
    elif update_type == 'update_signal_HRPT':
        names, filter_of = find_satellites(cd_sat, signal_type='HRPT')
        keyboard = kb.signal_HRPT_orbits
    elif update_type == 'update_signal_LRPT':
        names, filter_of = find_satellites(cd_sat, signal_type='LRPT')
        keyboard = kb.signal_LRPT_orbits
    elif update_type == 'update_group_NOAA':
        names, filter_of = find_satellites(cd_sat, group='NOAA')
        keyboard = kb.group_NOAA_orbits
    elif update_type == 'update_group_Meteor':
        names, filter_of = find_satellites(cd_sat, group='Meteor')
        keyboard = kb.group_Meteor_orbits
    elif update_type == 'update_satellite_NOAA_15':
        names, filter_of = find_satellites(cd_sat, name='NOAA 15')
        keyboard = kb.NOAA_15_orbits
    elif update_type == 'update_satellite_NOAA_18':
        names, filter_of = find_satellites(cd_sat, name='NOAA 18')
        keyboard = kb.NOAA_18_orbits
    elif update_type == 'update_satellite_NOAA_19':
        names, filter_of = find_satellites(cd_sat, name='NOAA 19')
        keyboard = kb.NOAA_19_orbits
    elif update_type == 'update_satellite_NOAA_20':
        names, filter_of = find_satellites(cd_sat, name='NOAA 20 (JPSS-1)')
        keyboard = kb.NOAA_20_orbits
    elif update_type == 'update_satellite_NOAA_21':
        names, filter_of = find_satellites(cd_sat, name='NOAA 21 (JPSS-2)')
        keyboard = kb.NOAA_21_orbits
    elif update_type == 'update_satellite_METEOR_M_2':
        names, filter_of = find_satellites(cd_sat, name='METEOR-M 2')
        keyboard = kb.METEOR_M_2_orbits
    elif update_type == 'update_satellite_METEOR_M2_2':
        names, filter_of = find_satellites(cd_sat, name='METEOR-M2 2')
        keyboard = kb.METEOR_M2_2_orbits
    else:
        names, filter_of = find_satellites(cd_sat)
        keyboard = kb.all_orbit
    
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
    
    await callback.message.delete()
    
    await callback.message.answer_photo(photo=buffer, caption=text, reply_markup=keyboard)
    await callback.answer()

@router.message(F.text == "нужна правда")
async def secret_menu_handler(message: Message):
    text = "Выберите действие:"
    keyboard = kb.secret_menu  
    
    await message.delete()
    await message.answer(text, reply_markup=keyboard)

@router.callback_query(F.data.in_({
    "tech_data", 
    "refresh_calculations", 
    "send_http_request", 
    "check_files", 
    "rebot"
}))

async def handle_secret_menu_buttons(callback: CallbackQuery, obs_lon: float = None, obs_lat: float = None, 
                                   obs_alt: float = None, end_time_hours: int = None):
    action = callback.data
    parse_mode = None
    keyboard = kb.back_to_secret_menu
    text = ""
    
    if action == "tech_data":
        await callback.message.delete()
        with open(cd_logs_tech, 'r', encoding='utf-8') as f:
            text = f.read() + '\n\n'
        with open(cd_logs_back, 'r', encoding='utf-8') as f:  
            text += 'Логи фонового процесса: \n'
            text += f.read()
        with open(cd_logs_htpp, 'r', encoding='utf-8') as f:
            text += '\n\nЛоги http сервера: \n'
            text += f.read()
        with open(cd_logs_decode, 'r', encoding='utf-8') as f:
            text += '\n\nЛоги функций записи и декодинга спутников: \n'
            text += f.read()

        
    elif action == "refresh_calculations":
        await callback.answer("Идет загрузка, подождите...")
        await callback.message.delete()
        text = "Вычисления обновлены"
        make_all_calculations_ones(obs_lon, obs_lat, obs_alt, end_time_hours)

    elif action == "send_http_request":
        await callback.answer("Идет загрузка, подождите...")
        await callback.message.delete()
        text = "HTPP запрос отправлен, проверьте логи"
        process_urls()
        
    elif action == "check_files":
        await callback.answer("Идет загрузка, подождите...")
        await callback.message.delete()
        sats = json_to_py(cd_sat)
        tles = json_to_py(cd_tle)
        coordinates = json_to_py(cd_coordinates)
        passes = json_to_py(cd_passes)
        text = "Результаты наличия проверки на наличие информации:\n\n"
        text += f'Всего в проекте задействовано {len(sats)} спутников\n' 
        text += f'В tles.json находится {len(tles)} спутников\n'
        text += f'В coordinates.json находится {len(coordinates)} спутников\n'
        text += f'В passes.json находится {len(passes)} спутников\n'
    
    
    await callback.message.answer(text, parse_mode=parse_mode, reply_markup=keyboard)
    await callback.answer()