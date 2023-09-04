from aiogram.types import BotCommand
from lexicon.Lexicon import list_command


# Функция для настройки кнопки Menu бота
def set_menu():
    return [BotCommand(command=command, description=description) for command, description in list_command.items()]
