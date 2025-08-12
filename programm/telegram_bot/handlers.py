import os
import time
from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, BufferedInputFile
from aiogram.filters import Command

import telegram_bot.keybords as kb 
from storage import json_to_py, find_satellites
from tracking.utils import (find_next_passes_for_satellites, find_next_passes_for_one_satellite,  
                            filter_by_names)
from tracking.visualization import orbits_and_legend

cd = os.getcwd() 
cd_sat = os.path.join(cd, 'programm', 'data', 'data_base', 'satellites.json')
cd_tle = os.path.join(cd, 'programm', 'data', 'data_base', 'tle.json')
cd_processing = os.path.join(cd, 'programm', 'data', 'data_base', 'processing.json')
cd_coordinates = os.path.join(cd, 'programm', 'data', 'data_base', 'coordinates.json')
cd_passes = os.path.join(cd, 'programm', 'data', 'data_base', 'passes.json')
cd_config = os.path.join(cd, 'programm', 'config.json')

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer('Меню', reply_markup=kb.menu)

##КНОПКИ НАЗАД
@router.callback_query(F.data == 'back_to_filter')
async def back_to_filter(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer('Выберите какие пролеты вас интересуют', reply_markup=kb.filter)
    await callback.answer()

@router.callback_query(F.data == 'back_to_group')
async def back_to_group(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer('Выберите группу спутников', reply_markup=kb.group)
    await callback.answer()

@router.callback_query(F.data == 'back_to_frequency')
async def back_to_frequency(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer('Выберите частоту', reply_markup=kb.frequency)
    await callback.answer()

@router.callback_query(F.data == 'back_to_signal')
async def back_to_signal(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer('Выберите тип сигнала', reply_markup=kb.type_signal)
    await callback.answer()

@router.callback_query(F.data == 'back_to_satellite')
async def back_to_satellite(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer('Выберите спутник', reply_markup=kb.names)
    await callback.answer()

@router.callback_query(F.data == 'back')
async def back(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer('Главное меню', reply_markup=kb.menu)
    await callback.answer()


@router.callback_query(F.data.in_(["satellites_base", "about", 'orbits', 'passes', 'photos']))
async def menu(callback: CallbackQuery):
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

        await callback.message.delete()
        await callback.message.answer(text, parse_mode="Markdown", reply_markup=kb.back)  
    elif callback.data == 'about':
        await callback.message.delete()
        await callback.message.answer(
            'Проект автоматически рассчитывает орбиты спутников, ' \
            'визуализирует их на карте, обрабатывает и декодирует изображения, принимаемыми со спутников.'
            , reply_markup=kb.back)
        
    elif callback.data == 'passes':
        await callback.message.delete()
        await callback.message.answer('Выберите какие пролеты вас интерисуют', reply_markup=kb.filter)

    elif callback.data == 'orbits':
        await callback.message.delete()
        await callback.message.answer('Выберите какие орбиты вас интерисуют', reply_markup=kb.orbits)

    await callback.answer()


@router.callback_query(F.data.in_(['filter_names', 'filter_frequency', 'filter_signal_type', 'filter_group', 'satellite_passes']))
async def handle_filters(callback: CallbackQuery):
    if callback.data == 'filter_names':
        names, filter_of = find_satellites(cd_sat)
        next_passes = find_next_passes_for_satellites(json_to_py(cd_passes), names)
        
        text = "Ближайшие пролеты спутников:\n\n"
        for passe in next_passes:
            text += f"{passe}\n\n"
        
        await callback.message.delete()
        await callback.message.answer(text, reply_markup=kb.back_to_filter)
        
    elif callback.data == 'filter_frequency':
        await callback.message.delete()
        await callback.message.answer("Выберите частоту:", reply_markup=kb.frequency)
        
    elif callback.data == 'filter_signal_type':
        await callback.message.delete()
        await callback.message.answer("Выберите тип сигнала:", reply_markup=kb.type_signal)
    
    elif callback.data == 'filter_group':
        await callback.message.delete()
        await callback.message.answer("Выберите группу:", reply_markup=kb.group)
        
    elif callback.data == 'satellite_passes':
        await callback.message.delete()
        await callback.message.answer("Введите название спутника для поиска пролетов:", reply_markup=kb.names)
        
    await callback.answer()

@router.callback_query(F.data.in_({'freq_137', 'freq_1700'}))
async def passes_freq(callback: CallbackQuery):
    if callback.data == 'freq_137':
        frequency = 137
    elif callback.data == 'freq_1700':
        frequency = 1698
    
    names, filter_of = find_satellites(cd_sat, frequency=frequency)
    next_passes = find_next_passes_for_satellites(json_to_py(cd_passes), names)
    text = f"Ближайшие пролеты спутников, отсортированные по {filter_of[0]}:\n\n"
    for passe in next_passes:
        text += f"{passe}\n\n"
    
    await callback.message.delete()
    await callback.message.answer(text, reply_markup=kb.back_to_frequency)

@router.callback_query(F.data.in_({'signal_APT', 'signal_HRPT', 'signal_LRPT'}))
async def passes_signal(callback: CallbackQuery):
    if callback.data == 'signal_APT':
        signal_type = 'APT'
    elif callback.data == 'signal_HRPT':
        signal_type = 'HRPT'
    elif callback.data == 'signal_LRPT':
        signal_type = 'LRPT'
    
    names, filter_of = find_satellites(cd_sat, signal_type=signal_type)
    next_passes = find_next_passes_for_satellites(json_to_py(cd_passes), names)
    text = f"Ближайшие пролеты спутников, отсортированные по {filter_of[0]}:\n\n"
    for passe in next_passes:
        text += f"{passe}\n\n"
    
    await callback.message.delete()
    await callback.message.answer(text, reply_markup=kb.back_to_signal)

@router.callback_query(F.data.in_({'group_NOAA', 'group_Meteor'}))
async def passes_group(callback: CallbackQuery):
    if callback.data == 'group_NOAA':
        group_name = 'NOAA'
    elif callback.data == 'group_Meteor':
        group_name = 'Meteor'
    
    names, filter_of = find_satellites(cd_sat, group=group_name)
    next_passes = find_next_passes_for_satellites(json_to_py(cd_passes), names)
    text = f"Ближайшие пролеты спутников, отсортированные по {filter_of[0]}:\n\n"
    for passe in next_passes:
        text += f"{passe}\n\n"
    
    await callback.message.delete()
    await callback.message.answer(text, reply_markup=kb.back_to_group)

@router.callback_query(F.data.in_({
    'NOAA 15', 'NOAA 18', 'NOAA 19', 
    'NOAA 20 (JPSS-1)', 'NOAA 21 (JPSS-2)', 
    'METEOR-M 2', 'METEOR-M2 2'
}))
async def passes_satellite(callback: CallbackQuery):
    satellite_name = callback.data  
    next_passes = find_next_passes_for_one_satellite(satellite_name, json_to_py(cd_passes))
    text = f"Ближайшие пролеты {satellite_name}:\n\n"
    for passe in next_passes:
        text += f"{passe}\n\n"
    
    await callback.message.delete()
    await callback.message.answer(text, reply_markup=kb.back_to_satellite)

@router.callback_query(F.data.in_({"orbits_all_2h", "orbits_specific", "orbits_by_type"}))
async def orbits_handler(
    callback: CallbackQuery,
    sats_coors: list,       
    step: int,
    obs_lon: float,
    obs_lat: float,
    sats_tle: dict,
    passes: dict
):
    unix_time_now = time.time()
    await callback.message.delete()

    if callback.data == 'orbits_all_2h':
        names, filter_of = find_satellites(cd_sat)
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
        await callback.message.answer_photo(photo=buffer, caption=text, reply_markup=kb.back)

    elif callback.data == 'orbits_specific':
        await callback.message.answer("Выберите спутник:", reply_markup=kb.names)
    elif callback.data == 'orbits_by_type':
        await callback.message.answer("Выберите тип орбиты:", reply_markup=kb.group)

    await callback.answer()