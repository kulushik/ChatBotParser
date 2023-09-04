from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder


def create_inline_kb(width: int, last_btn: str = None, **kwargs):
    # Инициализируем билдер
    kb_builder = InlineKeyboardBuilder()
    # Инициализируем список для кнопок
    buttons = []

    # Заполняем список кнопками из аргументов kwargs
    for button, text in kwargs.items():
        buttons.append(types.InlineKeyboardButton(text=text, callback_data=button))

    # Распаковываем список с кнопками в билдер методом row c параметром width
    kb_builder.row(*buttons, width=width)
    
    # Добавляем в билдер последнюю кнопку, если она передана в функцию
    if last_btn:
        kb_builder.row(types.InlineKeyboardButton(text=last_btn, callback_data='settings'))

    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()
