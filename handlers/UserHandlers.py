import logging
from aiogram import types, Router, F
from aiogram.filters import Command, CommandObject
from Config import ADMIN_ID
from keyboards import ReplyKeyboard, InlineKeyboard
from .CallbackHandlers import userCallbackRout
from .CallbackData import ChangeSheduleCallbackData
from lexicon.Lexicon import weekday_names, short_weekday_names, list_settings, help_msg
from logic.Parser import load_json
from logic.Setting import get_settings, register
from datetime import date

userRout = Router()
userRout.include_router(userCallbackRout)

@userRout.message(Command(commands=['start', 'help', 'day', 'week', 'bagreport', 'setting', 'change']))
async def event_command(message: types.Message, command: CommandObject):
    logging.info(f'Username: {message.from_user.username}, id: {message.from_user.id}, Имя: {message.from_user.full_name}: {message.text}')
    # command = message.text.split()[0]
    if command.command == 'start':
        await welcome(message)
        register(message.from_user.id, message.from_user.full_name, message.from_user.username)
    elif command.command == 'help':
        await help(message)
    elif command.command == 'day':
        await day(message)
    elif command.command == 'week':
        await week(message)
    elif command.command == 'bagreport':
        await bagreport(message)
    elif command.command == 'setting':
        await setting(message)
    elif command.command == 'change':
        await change_shedule(message)


# Обрабатываем команду /start
async def welcome(message: types.Message):
    await message.answer_photo('AgACAgIAAxkDAAIBkmTkd6qjj21R2eiL_WgzLUYT70geAAK5yzEblYQoS_Aeb-xn-Zs4AQADAgADcwADMAQ', 'Йоу')
    # await message.answer_photo(types.FSInputFile(r'img\statham.jpg'), 'Йоу')
    await help(message)
    await replace_keyboard(message, True)


# Обрабатываем команду /help
async def help(message: types.Message):
    await message.answer(text=help_msg)


# Обрабатываем команду /bagreport
async def bagreport(message: types.Message):
    try:
        report = message.text.split(' ', 1)[1]
        await message.bot.send_message(chat_id = ADMIN_ID, text = f'Баг репорт от пользователя Username: {message.from_user.username}, id: {message.from_user.id}, Имя: {message.from_user.full_name}:\n{report}')
        await message.answer('Информация передана!')
    except IndexError:
        await message.answer('Вы не ввели информацию об ошибке!\nСинтаксис данной команды:\n/bagreport [information]\n[information] - ваше сообщение об ошибке')


# Обрабатываем команду /setting
async def setting(message: types.Message):
    kb = InlineKeyboard.create_inline_kb(1, **list_settings, exit='🔚')
    await message.answer('Настройки:', reply_markup=kb)


# Обрабатываем команду /change
async def change_shedule(message: types.Message):
    kb = InlineKeyboard.create_inline_kb(3, **{ChangeSheduleCallbackData(change='add', week='', day='').pack():'Добавить', ChangeSheduleCallbackData(change='edit', week='', day='').pack():'Изменить', ChangeSheduleCallbackData(change='delete', week='', day='').pack():'Удалить'}, exit='🔚')
    await message.answer('Редактирование расписания\nIn developing...', reply_markup=kb)


# Смена клавиатуры
@userRout.message(F.text.in_({'<- Текущая неделя', 'Следующая неделя ->'}))
async def replace_keyboard(message: types.Message, cur_week: bool = True):
    if message.text == 'Следующая неделя ->' or cur_week == False:
        kb = ReplyKeyboard.kb_for_next_week()
        text = 'Выбрана следующая неделя'
    else:
        kb = ReplyKeyboard.kb_for_cur_week()
        text = 'Выбрана текущая неделя'

    await message.answer(text, reply_markup=kb)


# userRout.message.register(week, F.text.regexp('(?i)^неделя$'))
# userRout.message.register(week, F.text.regexp('(?i)^⠀?неделя⠀?$'))
# userRout.message.register(day, F.text.regexp('(?i)^⠀?(?:пн|вт|ср|чт|пт|сб|день)⠀?$'))
# userRout.message.register(day, F.text.regexp('(?i)^⠀(?:пн|вт|ср|чт|пт|сб)⠀$'))


# Обрабатываем команду /day
@userRout.message(F.text.regexp('(?i)^⠀?(?:пн|вт|ср|чт|пт|сб|день)⠀?$'))
async def day(message: types.Message):
    if '⠀' in message.text:
        week = 'next_week'
        msg = message.text.replace('⠀', '')
    else:
        week = 'current_week'
        msg = message.text

    if msg.lower() in ['пн', 'вт', 'ср', 'чт', 'пт', 'сб']:
        day = load_json(week, short_weekday_names[msg.lower()])
    else:
        day = load_json(week, weekday_names[date.today().weekday()])

    kol_msg = -1
    if day:
        if get_settings(message.from_user.id, 'day_block_messages'):
            block = '-'*20+'\n'
            for d in day[0]:
                if 'серверная' in d.lower() and message.from_user.id != 493465069:
                    continue
                block += d+'\n'+'-'*20+'\n'
                kol_msg +=1
            if kol_msg > 0:
                await message.answer(block)
            del block
        else:
            for d in day[0]:
                if 'серверная' in d.lower() and message.from_user.id != 493465069:
                    continue
                await message.answer('-'*20+'\n'+d+'\n'+'-'*20)
                kol_msg +=1

    if kol_msg <= 0:
        await message.answer_photo('AgACAgIAAxkBAAIBomTkjeKcONYR6fiT1tO8S4J_hA-1AAJyzDEblYQoS2ubmFWfn8OIAQADAgADcwADMAQ', 'Староста разрешает сегодня не ходить😎')
        # await message.answer_photo(types.FSInputFile(r'img\today.jpg'), 'Староста разрешает сегодня не ходить😎')


# Обрабатываем команду /week
@userRout.message(F.text.regexp('(?i)^⠀?неделя⠀?$'))
async def week(message: types.Message):
    if '⠀' in message.text:
        week = 'next_week'
    else:
        week = 'current_week'

    full_week = load_json(week)

    if get_settings(message.from_user.id, 'week_block_messages'):
        block = ''
        for row in full_week:
            block += '-'*20+'\n'
            for item in row:
                block += item+'\n'+'-'*20+'\n'
            block +='\n'
        await message.answer(block)
    else:
        for row in full_week:
            block = '-'*20+'\n'
            for item in row:
                block += item+'\n'+'-'*20+'\n'
            await message.answer(block)


# Обрабатываем все входящие сообщения
@userRout.message()
async def echo(message: types.Message):
    await message.answer_photo('AgACAgIAAxkDAAIBiGTkcMPDBofITTH3C-u3Nhet6KxvAALAyzEblYQoS5BHtx_E4tkdAQADAgADcwADMAQ', 'Зачем ты сюда пишешь? Держи обои на рабочий стол :)')
    # photo = await message.answer_photo(types.FSInputFile(r'img\desktop.png'), 'Зачем ты сюда пишешь? Держи обои на рабочий стол :)')
    logging.info(f'Username: {message.from_user.username}, id: {message.from_user.id}, Имя: {message.from_user.full_name}: {message.text}')
