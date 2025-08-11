from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Орбиты спутников', callback_data='orbits'),
     InlineKeyboardButton(text='Фотографии со спутников', callback_data='photos')],
    [InlineKeyboardButton(text='База спутников', callback_data='satellites_base'),
     InlineKeyboardButton(text='Пролеты спутников', callback_data='passes')],
    [InlineKeyboardButton(text='О проекте', callback_data='about')]
])

orbits_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Орбиты всех спутников сейчас', callback_data='all_orbits_now')],
    [InlineKeyboardButton(text='Орбиты спутнику по группам', callback_data='orbits_by_groups')],
    [InlineKeyboardButton(text='Орбита одного спутника', callback_data='single_orbit')],
    [InlineKeyboardButton(text='Назад в главное меню', callback_data='main_menu')]
])

back = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Назад', callback_data='back')] 
])

filter = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Ближайшие пролеты каждого спутника', callback_data='filter_names')],
    [InlineKeyboardButton(text='По частоте', callback_data='filter_frequency'),
     InlineKeyboardButton(text='По типу сигнала', callback_data='filter_signal_type')],
    [InlineKeyboardButton(text='По группе', callback_data='filter_group'),
     InlineKeyboardButton(text='Пролеты конкретного спутника', callback_data='satellite_passes')],
    [InlineKeyboardButton(text='Назад', callback_data='back')]
])

frequency = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='137 МГц', callback_data='freq_137')],
    [InlineKeyboardButton(text='1.7 ГГц', callback_data='freq_1700')],
    [InlineKeyboardButton(text='Назад', callback_data='back_to_filter')]
])

type_signal = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='APT', callback_data='signal_APT')],
    [InlineKeyboardButton(text='HRPT', callback_data='signal_HRPT')],
    [InlineKeyboardButton(text='LRPT', callback_data='signal_LRPT')],
    [InlineKeyboardButton(text='Назад', callback_data='back_to_filter')]
])

group = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='NOAA', callback_data='group_NOAA')],
    [InlineKeyboardButton(text='Meteor', callback_data='group_Meteor')],
    [InlineKeyboardButton(text='Назад', callback_data='back_to_filter')]
])

back_to_filter = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Назад', callback_data='back_to_filter')] 
])

names = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='NOAA 15', callback_data='NOAA 15')],
    [InlineKeyboardButton(text='NOAA 18', callback_data='NOAA 18')],
    [InlineKeyboardButton(text='NOAA 19', callback_data='NOAA 19')],
    [InlineKeyboardButton(text='NOAA 20 (JPSS-1)', callback_data='NOAA 20 (JPSS-1)')],
    [InlineKeyboardButton(text='NOAA 21 (JPSS-2)', callback_data='NOAA 21 (JPSS-2)')],
    [InlineKeyboardButton(text='METEOR-M 2', callback_data='METEOR-M 2')],
    [InlineKeyboardButton(text='METEOR-M2 2', callback_data='METEOR-M2 2')],
    [InlineKeyboardButton(text='Назад', callback_data='back_to_filter')]
])