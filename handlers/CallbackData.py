from aiogram.filters.callback_data import CallbackData


class SettingsCallbackData(CallbackData, prefix='settings'):
    category: str
    choice: bool

""" Для уведомлений
Через инлайн кнопки:
    1. Выбор добавить/удалить/изменить
    2. Выбор недели текущая/следующая
    3. Выбор дня
    4. Выбор времени
        4.1 При добавлении: выборка среди пустых значений
        4.2 При удалении/изменении: выборка среди существующих значений

"""
class ChangeSheduleCallbackData(CallbackData, prefix='change'):
    change: str
    week: str
    day: str
