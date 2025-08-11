import os
from aiogram import Bot, Dispatcher, F, Router
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, CallbackQuery
from aiogram.filters import Command, CommandStart

import telegram_bot.keybords as kb 
from storage import json_to_py, find_satellites
from tracking.utils import find_next_passes_for_satellites, filter_by_names

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

@router.callback_query(F.data == 'back')
async def back(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer('Меню:', reply_markup=kb.menu)
    
    await callback.answer() 

@router.callback_query(F.data == 'back_to_filter')
async def back(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer('Выберите какие пролеты вас интерисуют', reply_markup=kb.filter)
    
    await callback.answer() 


@router.callback_query(F.data.in_(["satellites_base", "about", 'otbits', 'passes', 'photos']))
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
        await callback.message.answer(text, reply_markup=kb.back)
        
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
