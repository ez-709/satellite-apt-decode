from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def back_button(callback_data):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Назад', callback_data=callback_data)]
    ])

def with_back_button(buttons, back_callback):
    return InlineKeyboardMarkup(inline_keyboard=buttons + [
        [InlineKeyboardButton(text='Назад', callback_data=back_callback)]
    ])

menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Орбиты спутников', callback_data='orbits'),
     InlineKeyboardButton(text='Фотографии со спутников', callback_data='photos')],
    [InlineKeyboardButton(text='База спутников', callback_data='satellites_base'),
     InlineKeyboardButton(text='Пролеты спутников', callback_data='passes')],
    [InlineKeyboardButton(text='О проекте', callback_data='about')]
])

back = back_button('back')
back_to_filter_passes = back_button('back_to_filter_passes')
back_to_group_passes = back_button('back_to_group_passes')
back_to_names_passes = back_button('back_to_names_passes')
back_to_frequency_passes = back_button('back_to_frequency_passes')
back_to_signal_passes = back_button('back_to_signal_passes')
back_to_orbits = back_button('back_to_orbits')
back_to_orbits_filter = back_button('back_to_orbits_filter')
back_to_group_orbits = back_button('back_to_group_orbits')
back_to_frequency_orbits = back_button('back_to_frequency_orbits')
back_to_signal_orbits = back_button('back_to_signal_orbits')
back_to_names_orbits = back_button('back_to_names_orbits')

filter_passes = with_back_button([
    [InlineKeyboardButton(text='Ближайшие пролеты каждого спутника', callback_data='filter_names_passes')],
    [InlineKeyboardButton(text='По частоте', callback_data='filter_frequency_passes'),
     InlineKeyboardButton(text='По типу сигнала', callback_data='filter_signal_type_passes')],
    [InlineKeyboardButton(text='По группе', callback_data='filter_group_passes'),
     InlineKeyboardButton(text='Пролеты конкретного спутника', callback_data='satellite_passes')]
], 'back')

frequency_passes = with_back_button([
    [InlineKeyboardButton(text='137 МГц', callback_data='freq_137_passes')],
    [InlineKeyboardButton(text='1.7 ГГц', callback_data='freq_1700_passes')]
], 'back_to_filter_passes')

type_signal_passes = with_back_button([
    [InlineKeyboardButton(text='APT', callback_data='signal_APT_passes')],
    [InlineKeyboardButton(text='HRPT', callback_data='signal_HRPT_passes')],
    [InlineKeyboardButton(text='LRPT', callback_data='signal_LRPT_passes')]
], 'back_to_filter_passes')

group_passes = with_back_button([
    [InlineKeyboardButton(text='NOAA', callback_data='group_NOAA_passes')],
    [InlineKeyboardButton(text='Meteor', callback_data='group_Meteor_passes')]
], 'back_to_filter_passes')

names_passes = with_back_button([
    [InlineKeyboardButton(text='NOAA 15', callback_data='NOAA 15_passes')],
    [InlineKeyboardButton(text='NOAA 18', callback_data='NOAA 18_passes')],
    [InlineKeyboardButton(text='NOAA 19', callback_data='NOAA 19_passes')],
    [InlineKeyboardButton(text='NOAA 20 (JPSS-1)', callback_data='NOAA 20 (JPSS-1)_passes')],
    [InlineKeyboardButton(text='NOAA 21 (JPSS-2)', callback_data='NOAA 21 (JPSS-2)_passes')],
    [InlineKeyboardButton(text='METEOR-M 2', callback_data='METEOR-M 2_passes')],
    [InlineKeyboardButton(text='METEOR-M2 2', callback_data='METEOR-M2 2_passes')]
], 'back_to_filter_passes')

orbits = with_back_button([
    [InlineKeyboardButton(text="Все спутники (2 часа)", callback_data="orbits_all_2h")],
    [InlineKeyboardButton(text="Орбиты спутников, отсортированные по:", callback_data="orbits_by_filter")], 
    [InlineKeyboardButton(text="Орбита конкретного спутника", callback_data="orbits_one_satellite")]
], 'back')

all_orbit = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Обновить карту', callback_data='update_orbit_all')],
    [InlineKeyboardButton(text='Назад', callback_data='back_to_orbits')] 
])

freq_orbit = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Обновить карту', callback_data='update_orbit_freq')],
    [InlineKeyboardButton(text='Назад', callback_data='back_to_orbits_freq')] 
])

freq_orbit_back = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Обновить карту', callback_data='update_orbit_freq')],
    [InlineKeyboardButton(text='Назад', callback_data='back_to_orbits_freq')] 
])

signal_orbit_back = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Обновить карту', callback_data='update_orbit_signal')],
    [InlineKeyboardButton(text='Назад', callback_data='back_to_signal_orbits')] 
])

group_orbit_back = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Обновить карту', callback_data='update_orbit_group')],
    [InlineKeyboardButton(text='Назад', callback_data='back_to_group_orbits')] 
])

satellite_orbit_back = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Обновить карту', callback_data='update_orbit_satellite')],
    [InlineKeyboardButton(text='Назад', callback_data='back_to_names_orbits')] 
])

filter_orbits = with_back_button([
    [InlineKeyboardButton(text='По частоте', callback_data='filter_frequency_orbits')],
    [InlineKeyboardButton(text='По типу сигнала', callback_data='filter_signal_type_orbits')],
    [InlineKeyboardButton(text='По группе', callback_data='filter_group_orbits')]
], 'back_to_orbits')

frequency_orbits = with_back_button([
    [InlineKeyboardButton(text='137 МГц', callback_data='freq_137_orbits')],
    [InlineKeyboardButton(text='1.7 ГГц', callback_data='freq_1700_orbits')]
], 'back_to_orbits_filter')

type_signal_orbits = with_back_button([
    [InlineKeyboardButton(text='APT', callback_data='signal_APT_orbits')],
    [InlineKeyboardButton(text='HRPT', callback_data='signal_HRPT_orbits')],
    [InlineKeyboardButton(text='LRPT', callback_data='signal_LRPT_orbits')]
], 'back_to_orbits_filter')

group_orbits = with_back_button([
    [InlineKeyboardButton(text='NOAA', callback_data='group_NOAA_orbits')],
    [InlineKeyboardButton(text='Meteor', callback_data='group_Meteor_orbits')]
], 'back_to_orbits_filter')

names_orbits = with_back_button([
    [InlineKeyboardButton(text='NOAA 15', callback_data='NOAA 15_orbits')],
    [InlineKeyboardButton(text='NOAA 18', callback_data='NOAA 18_orbits')],
    [InlineKeyboardButton(text='NOAA 19', callback_data='NOAA 19_orbits')],
    [InlineKeyboardButton(text='NOAA 20 (JPSS-1)', callback_data='NOAA 20 (JPSS-1)_orbits')],
    [InlineKeyboardButton(text='NOAA 21 (JPSS-2)', callback_data='NOAA 21 (JPSS-2)_orbits')],
    [InlineKeyboardButton(text='METEOR-M 2', callback_data='METEOR-M 2_orbits')],
    [InlineKeyboardButton(text='METEOR-M2 2', callback_data='METEOR-M2 2_orbits')]
], 'back_to_orbits')