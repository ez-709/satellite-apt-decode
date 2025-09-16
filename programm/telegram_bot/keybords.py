from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

def back_button(text):
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text=text)]
    ], resize_keyboard=True)

def with_back_button(buttons, back_text):
    keyboard = []
    for row in buttons:
        keyboard_row = []
        for button in row:
            keyboard_row.append(KeyboardButton(text=button.text))
        keyboard.append(keyboard_row)
    keyboard.append([KeyboardButton(text=back_text)])
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Орбиты спутников'), KeyboardButton(text='Фотографии со спутников')],
    [KeyboardButton(text='База спутников'), KeyboardButton(text='Пролеты спутников')],
    [KeyboardButton(text='О проекте')]
], resize_keyboard=True)

back = back_button('Назад')
back_to_filter_passes = back_button('Назад')
back_to_group_passes = back_button('Назад')
back_to_names_passes = back_button('Назад')
back_to_frequency_passes = back_button('Назад')
back_to_signal_passes = back_button('Назад')
back_to_orbits = back_button('Назад')
back_to_orbits_filter = back_button('Назад')
back_to_group_orbits = back_button('Назад')
back_to_frequency_orbits = back_button('Назад')
back_to_signal_orbits = back_button('Назад')
back_to_names_orbits = back_button('Назад')
back_to_secret_menu = back_button('Назад')

filter_passes = with_back_button([
    [KeyboardButton(text='Ближайшие пролеты каждого спутника')],
    [KeyboardButton(text='По частоте'), KeyboardButton(text='По типу сигнала')],
    [KeyboardButton(text='По группе'), KeyboardButton(text='Пролеты конкретного спутника')]
], 'Назад')

frequency_passes = with_back_button([
    [KeyboardButton(text='137 МГц')],
    [KeyboardButton(text='1.7 ГГц')]
], 'Назад')

type_signal_passes = with_back_button([
    [KeyboardButton(text='APT')],
    [KeyboardButton(text='HRPT')],
    [KeyboardButton(text='LRPT')]
], 'Назад')

group_passes = with_back_button([
    [KeyboardButton(text='NOAA')],
    [KeyboardButton(text='Meteor')]
], 'Назад')

names_passes = with_back_button([
    [KeyboardButton(text='NOAA 15')],
    [KeyboardButton(text='NOAA 18')],
    [KeyboardButton(text='NOAA 19')],
    [KeyboardButton(text='NOAA 20 (JPSS-1)')],
    [KeyboardButton(text='NOAA 21 (JPSS-2)')],
    [KeyboardButton(text='METEOR-M 2')],
    [KeyboardButton(text='METEOR-M2 2')]
], 'Назад')

orbits = with_back_button([
    [KeyboardButton(text="Все спутники (2 часа)")],
    [KeyboardButton(text="Орбиты спутников, отсортированные по:")], 
    [KeyboardButton(text="Орбита конкретного спутника")]
], 'Назад')

NOAA_15_orbits = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Обновить карту')],
    [KeyboardButton(text='Назад')] 
], resize_keyboard=True)

NOAA_18_orbits = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Обновить карту')],
    [KeyboardButton(text='Назад')] 
], resize_keyboard=True)

NOAA_19_orbits = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Обновить карту')],
    [KeyboardButton(text='Назад')] 
], resize_keyboard=True)

NOAA_20_orbits = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Обновить карту')],
    [KeyboardButton(text='Назад')] 
], resize_keyboard=True)

NOAA_21_orbits = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Обновить карту')],
    [KeyboardButton(text='Назад')] 
], resize_keyboard=True)

METEOR_M_2_orbits = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Обновить карту')],
    [KeyboardButton(text='Назад')] 
], resize_keyboard=True)

METEOR_M2_2_orbits = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Обновить карту')],
    [KeyboardButton(text='Назад')] 
], resize_keyboard=True)

freq_137_orbits = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Обновить карту')],
    [KeyboardButton(text='Назад')] 
], resize_keyboard=True)

freq_1700_orbits = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Обновить карту')],
    [KeyboardButton(text='Назад')] 
], resize_keyboard=True)

group_NOAA_orbits = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Обновить карту')],
    [KeyboardButton(text='Назад')] 
], resize_keyboard=True)

group_Meteor_orbits = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Обновить карту')],
    [KeyboardButton(text='Назад')] 
], resize_keyboard=True)

signal_APT_orbits = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Обновить карту')],
    [KeyboardButton(text='Назад')] 
], resize_keyboard=True)

signal_HRPT_orbits = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Обновить карту')],
    [KeyboardButton(text='Назад')] 
], resize_keyboard=True)

signal_LRPT_orbits = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Обновить карту')],
    [KeyboardButton(text='Назад')] 
], resize_keyboard=True)

all_orbit = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Обновить карту')],
    [KeyboardButton(text='Назад')] 
], resize_keyboard=True)

freq_orbit_back = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Обновить карту')],
    [KeyboardButton(text='Назад')] 
], resize_keyboard=True)

signal_orbit_back = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Обновить карту')],
    [KeyboardButton(text='Назад')] 
], resize_keyboard=True)

group_orbit_back = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Обновить карту')],
    [KeyboardButton(text='Назад')] 
], resize_keyboard=True)

satellite_orbit_back = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Обновить карту')],
    [KeyboardButton(text='Назад')] 
], resize_keyboard=True)

filter_orbits = with_back_button([
    [KeyboardButton(text='По частоте')],
    [KeyboardButton(text='По типу сигнала')],
    [KeyboardButton(text='По группе')]
], 'Назад')

frequency_orbits = with_back_button([
    [KeyboardButton(text='137 МГц')],
    [KeyboardButton(text='1.7 ГГц')]
], 'Назад')

type_signal_orbits = with_back_button([
    [KeyboardButton(text='APT')],
    [KeyboardButton(text='HRPT')],
    [KeyboardButton(text='LRPT')]
], 'Назад')

group_orbits = with_back_button([
    [KeyboardButton(text='NOAA')],
    [KeyboardButton(text='Meteor')]
], 'Назад')

names_orbits = with_back_button([
    [KeyboardButton(text='NOAA 15')],
    [KeyboardButton(text='NOAA 18')],
    [KeyboardButton(text='NOAA 19')],
    [KeyboardButton(text='NOAA 20 (JPSS-1)')],
    [KeyboardButton(text='NOAA 21 (JPSS-2)')],
    [KeyboardButton(text='METEOR-M 2')],
    [KeyboardButton(text='METEOR-M2 2')]
], 'Назад')

secret_menu = with_back_button([
    [KeyboardButton(text='Технические данные')],
    [KeyboardButton(text='Обновить расчёты')],
    [KeyboardButton(text='Отправить HTTP-запрос по спутникам')],
    [KeyboardButton(text='Проверить наличие содержимого файлов')]
], 'Назад')