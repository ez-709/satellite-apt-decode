import asyncio
import numpy as np
from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import Message, CallbackQuery, InputMediaPhoto, InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile
import matplotlib
matplotlib.use('Agg')  # Устанавливаем backend без GUI
import matplotlib.pyplot as plt
import os
from tracking.utils import *
from storage import *

cd = os.getcwd() 
cd_sat = os.path.join(cd, 'programm', 'data', 'data_base', 'satellites.json')
cd_tle = os.path.join(cd, 'programm', 'data', 'data_base', 'tle.json')
cd_processing = os.path.join(cd, 'programm', 'data', 'data_base', 'processing.json')
cd_coordinates = os.path.join(cd, 'programm', 'data', 'data_base', 'coordinates.json')
cd_passes = os.path.join(cd, 'programm', 'data', 'data_base', 'passes.json')
cd_config = os.path.join(cd, 'programm', 'config.json')


name = 'NOAA 15'
passes = find_next_passes_for_one_satellite(name, json_to_py(cd_passes))
print(passes)