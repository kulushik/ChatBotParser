from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram.client.session.aiohttp import AiohttpSession
from logic.Parser import get_schedule_in_json
from aiogram import Bot, Dispatcher
from handlers import AdminHandlers, UserHandlers
from keyboards.MenuKeyboard import set_menu
import Config
import asyncio
import logging
from datetime import datetime, date, time
import math


# Добавление обработчика логов
logger = logging.getLogger('')
logger.setLevel(logging.INFO)

handler = logging.FileHandler(filename=f'logs\\{str(date.today())}.log', encoding='utf-8')
handler.setFormatter(logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%d-%m-%Y %H:%M:%S'))

logger.addHandler(handler)

# Инициализируем бота и диспетчер
async def main():
    session = AiohttpSession(proxy=Config.PROXY)
    bot = Bot(token=Config.TOKEN, session=session, parse_mode='HTML')
    dp = Dispatcher()

    await bot.set_my_commands(set_menu())

    dp.include_router(AdminHandlers.adminRout)
    dp.include_router(UserHandlers.userRout)

    await dp.start_polling(bot)


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
    asyncio.run(main())
    # dp.run_polling(bot)
