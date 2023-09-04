from aiogram import types, Router, F
from aiogram.filters import Command
from logic.Parser import get_schedule_in_json
from Config import ADMIN_ID


adminRout = Router()
adminRout.message.filter(F.from_user.id == ADMIN_ID)


@adminRout.message(Command(commands=['getfileid']))
async def get_id(message: types.Message):
    if message.photo:
        await message.answer(f'<code>{message.photo[0].file_id}</code>')
    if message.document:
        await message.answer(f'<code>{message.document.file_id}</code>')


@adminRout.message(Command(commands=['updatenow']))
async def update_now(message: types.Message):
    try:
        get_schedule_in_json()
        await message.answer('Успешно обновлено')
    except:
        await message.answer('Возникла какая-то проблема, чекай логи')

