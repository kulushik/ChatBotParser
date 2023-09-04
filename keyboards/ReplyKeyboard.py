from aiogram import types

def kb_for_cur_week():
    return types.ReplyKeyboardMarkup(keyboard=[[types.KeyboardButton(text='Следующая неделя ->')], [types.KeyboardButton(text=f'{day}') for day in ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб']], [types.KeyboardButton(text=f'{day}') for day in ['Неделя', 'День']]], resize_keyboard=True, input_field_placeholder='Текущая неделя:')


def kb_for_next_week():
    return types.ReplyKeyboardMarkup(keyboard=[[types.KeyboardButton(text='<- Текущая неделя')], [types.KeyboardButton(text=f'{day}') for day in ['⠀Пн⠀', '⠀Вт⠀', '⠀Ср⠀', '⠀Чт⠀', '⠀Пт⠀', '⠀Сб⠀']], [types.KeyboardButton(text='⠀Неделя⠀')]], resize_keyboard=True, input_field_placeholder='Следующая неделя:')