from apscheduler.schedulers.asyncio import AsyncIOScheduler
from Parser import get_schedule_in_json, load_json
from Setting import register, set_settings, get_settings
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.callback_data import CallbackData
import Config
import logging
from datetime import datetime, date, time
import math

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%d-%m-%Y %H:%M:%S')

# Добавление обработчика логов
handler = logging.FileHandler(f'logs\\{str(date.today())}.log')
#handler.setLevel(logging.INFO)
handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', '%d-%m-%Y %H:%M:%S'))
logging.getLogger('').addHandler(handler)

# Инициализируем бота и диспетчер
bot = Bot(token=Config.TOKEN, proxy=Config.PROXY, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

cb_data_notification = CallbackData('choice_notification', 'choice')
cb_data_day = CallbackData('choice_day_block', 'choice')
cb_data_week = CallbackData('choice_week_block', 'choice')

list_command = """Список команд:
1. /start - Начало работы
2. /help - Помощь по командам
3. /day - Расписание на текущий день
4. /week - Расписание на теущую неделю
5. /bagreport [information] - Cообщение для администратора с информацией об ошибке
6. /setting - Меню настроек
"""
weekday_names = ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота', 'воскресенье']
short_weekday_names = {'пн':'понедельник', 'вт':'вторник', 'ср':'среда', 'чт':'четверг', 'пт':'пятница', 'сб':'суббота', 'вс':'воскресенье'}
list_settings = {'notifications':'Уведомления', 'day_block_messages':'Цельное сообщение на день', 'week_block_messages':'Цельное сообщение на неделю'}

@dp.message_handler(commands=['start', 'help', 'day', 'week', 'bagreport', 'setting', 'updatenow'])
async def ivent_command(message: types.Message):
    logging.info(f'Username: {message.from_user.username}, id: {message.from_user.id}, Имя: {message.from_user.full_name}: {message.text}')
    command = message.text.split()[0]
    if command == '/start':
        await welcome(message)
        register(message.from_user.id, message.from_user.full_name, message.from_user.username)
    elif command == '/help':
        await help(message)
    elif command == '/day':
        await day(message)
    elif command == '/week':
        await week(message)
    elif command == '/bagreport':
        await bagreport(message)
    elif command == '/setting':
        await setting(message)
    elif command == '/updatenow':
        await update_now(message)


# Обрабатываем команду /start
async def welcome(message: types.Message):
    with open(r'img\statham.jpg', 'rb') as photo:
        await message.answer_photo(types.InputFile(photo), 'Йоу')
    await help(message)
    await replace_keyboard(message, True)


# Обрабатываем команду /help
async def help(message: types.Message):
    await message.answer(text=list_command)


# Обрабатываем команду /day
async def day(message: types.Message):
    if '⠀' in message.text:
        week = 'next_week'
        message.text = message.text.replace('⠀', '')
    else:
        week = 'current_week'

    if message.text.lower() in ['пн', 'вт', 'ср', 'чт', 'пт', 'сб']:
        day = load_json(week, short_weekday_names[message.text.lower()])
    else:
        day = load_json(week, weekday_names[date.today().weekday()])

    kol_msg = -1
    if day:
        if get_settings(message.from_user.id, 'day_block_messages'):
            block = '-'*20+'\n'
            for d in day[0]:
                if 'серверная' in d.lower() and message.from_id != 493465069:
                    continue
                block += d+'\n'+'-'*20+'\n'
                kol_msg +=1
            if kol_msg > 0:
                await message.answer(block)
            del block
        else:
            for d in day[0]:
                if 'серверная' in d.lower() and message.from_id != 493465069:
                    continue
                await message.answer('-'*20+'\n'+d+'\n'+'-'*20)
                kol_msg +=1

    if kol_msg <= 0:
        with open(r'img\today.jpg', 'rb') as photo:
            await message.answer_photo(types.InputFile(photo), 'Староста разрешает сегодня не ходить😎')


# Обрабатываем команду /week
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


# Обрабатываем команду /bagreport
async def bagreport(message: types.Message):
    try:
        report = message.text.split(' ', 1)[1]
        await bot.send_message(Config.ADMIN_ID, f'Баг репорт от пользователя Username: {message.from_user.username}, id: {message.from_user.id}, Имя: {message.from_user.full_name}:\n{report}')
        await message.answer('Информация передана!')
    except IndexError:
        await message.answer('Вы не ввели информацию об ошибке!\nСинтаксис данной команды:\n/bagreport [information]\n[information] - ваше сообщение об ошибке')


# Обрабатываем команду /updatenow
async def update_now(message: types.Message):
    try:
        get_schedule_in_json()
        await message.answer('Успешно обновлено')
    except:
        await message.answer('Возникла какая-то проблема, чекай логи')


### I n l i n e  K e y b o a r d ###

async def setting(message: types.Message, answer: bool = True):
    buttons = []
    for callback, text in list_settings.items():
        buttons.append([types.InlineKeyboardButton(text=text, callback_data=callback)])
    kb = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    if answer:
        await message.answer('Настройки:', reply_markup=kb)
    else:
        await message.edit_text('Настройки:', reply_markup=kb)

async def notification(message: types.Message):
    buttons =[[
        types.InlineKeyboardButton('Да', callback_data=cb_data_notification.new(choice='True')),
        types.InlineKeyboardButton('Нет', callback_data=cb_data_notification.new(choice='False'))
        ],
        [
            types.InlineKeyboardButton('<-- Назад', callback_data='settings')
        ]]
    kb = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    await message.edit_text('Хотите ли вы получать уведомления?', reply_markup=kb)

async def day_block(message: types.Message):
    buttons =[[
        types.InlineKeyboardButton('Да', callback_data=cb_data_day.new(choice='True')),
        types.InlineKeyboardButton('Нет', callback_data=cb_data_day.new(choice='False'))
        ],
        [
            types.InlineKeyboardButton('<-- Назад', callback_data='settings')
        ]]
    kb = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    await message.edit_text('Хотите ли вы получать цельные сообщения для расписания на день?', reply_markup=kb)

async def week_block(message: types.Message):
    buttons =[[
        types.InlineKeyboardButton('Да', callback_data=cb_data_week.new(choice='True')),
        types.InlineKeyboardButton('Нет', callback_data=cb_data_week.new(choice='False'))
        ],
        [
            types.InlineKeyboardButton('<-- Назад', callback_data='settings')
        ]]
    kb = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    await message.edit_text('Хотите ли вы получать цельные сообщения для расписания на неделю?', reply_markup=kb)

### I n l i n e  K e y b o a r d ###

### C a l l b a c k  Q u e r y ###

@dp.callback_query_handler(text='settings')
async def settings(callback: types.CallbackQuery):
    await setting(callback.message, False)
    await callback.answer()

@dp.callback_query_handler(text='notifications')
async def notifications(callback: types.CallbackQuery):
    await notification(callback.message)
    await callback.answer(f'Лол что... ну ты и размечтался(-лась) конечно...\nТы, конечно, можешь поменять настройки, но толку...', show_alert=True)

@dp.callback_query_handler(cb_data_notification.filter())
async def choice_notification(callback: types.CallbackQuery, callback_data: dict):
    set_settings(callback.from_user.id, 'notifications', eval(callback_data['choice']))

    if eval(callback_data['choice']) == True:
        await callback.answer('Уведомления включены', show_alert=True)
    else:
        await callback.answer('Уведомления отключены', show_alert=True)

@dp.callback_query_handler(cb_data_day.filter())
async def choice_block_day(callback: types.CallbackQuery, callback_data: dict):
    set_settings(callback.from_user.id, 'day_block_messages', eval(callback_data['choice']))

    if eval(callback_data['choice']) == True:
        await callback.answer('Цельные сообщения включены', show_alert=True)
    else:
        await callback.answer('Цельные сообщения отключены', show_alert=True)

@dp.callback_query_handler(cb_data_week.filter())
async def choice_block_week(callback: types.CallbackQuery, callback_data: dict):
    set_settings(callback.from_user.id, 'week_block_messages', eval(callback_data['choice']))

    if eval(callback_data['choice']) == True:
        await callback.answer('Цельные сообщения включены', show_alert=True)
    else:
        await callback.answer('Цельные сообщения отключены', show_alert=True)

@dp.callback_query_handler(text='day_block_messages')
async def day_block_messages(callback: types.CallbackQuery):
    await day_block(callback.message)
    await callback.answer()

@dp.callback_query_handler(text='week_block_messages')
async def day_block_messages(callback: types.CallbackQuery):
    await week_block(callback.message)
    await callback.answer()

### C a l l b a c k  Q u e r y ###


# Смена клавиатуры
@dp.message_handler(content_types=types.ContentType.TEXT, text=['<- Текущая неделя', 'Следующая неделя ->'])
async def replace_keyboard(message: types.Message, cur_week: bool = True):
    if message.text == 'Следующая неделя ->' or cur_week == False:
        kb = types.ReplyKeyboardMarkup(keyboard=[['<- Текущая неделя'], ['⠀Пн⠀', '⠀Вт⠀', '⠀Ср⠀', '⠀Чт⠀', '⠀Пт⠀', '⠀Сб⠀'], ['⠀Неделя⠀']], resize_keyboard=True, input_field_placeholder='Следующая неделя:')
        text = 'Выбрана следующая неделя'
    else:
        kb = types.ReplyKeyboardMarkup(keyboard=[['Следующая неделя ->'], ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб'], ['Неделя', 'День']], resize_keyboard=True, input_field_placeholder='Текущая неделя:')
        text = 'Выбрана текущая неделя'

    await message.answer(text, reply_markup=kb)


dp.register_message_handler(week, content_types=types.ContentType.TEXT, regexp='(?i)^неделя$')
dp.register_message_handler(week, content_types=types.ContentType.TEXT, regexp='(?i)^⠀неделя⠀$')
dp.register_message_handler(day, content_types=types.ContentType.TEXT, regexp='(?i)^(?:пн|вт|ср|чт|пт|сб|день)$')
dp.register_message_handler(day, content_types=types.ContentType.TEXT, regexp='(?i)^⠀(?:пн|вт|ср|чт|пт|сб)⠀$')

# Обрабатываем все входящие сообщения
@dp.message_handler()
async def echo(message: types.Message):
    with open(r'img\desktop.png', 'rb') as photo:
        await message.answer_photo(types.InputFile(photo), 'Зачем ты сюда пишешь? Держи обои на рабочий стол :)')
    logging.info(f'Username: {message.from_user.username}, id: {message.from_user.id}, Имя: {message.from_user.full_name}: {message.text}')


if __name__ == '__main__':
    # Создание планировщика
    scheduler = AsyncIOScheduler()
    # Установка начального времени
    interval = 4
    date_time = datetime.now()
    start_time = datetime.combine(date_time.date(), time(math.ceil(date_time.hour/interval)*interval))
    # Установка параметров планировщика
    scheduler.add_job(get_schedule_in_json, 'interval', hours=interval, start_date=start_time)
    # Запуск планировщика
    scheduler.start()

    # Запуск бота
    executor.start_polling(dp, skip_updates=False)
