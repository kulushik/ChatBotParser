from aiogram import types, Router, F
from keyboards import InlineKeyboard
from .CallbackData import SettingsCallbackData, ChangeSheduleCallbackData
from lexicon.Lexicon import list_settings
from logic.Change import check_day
from logic.Setting import set_settings


userCallbackRout = Router()

@userCallbackRout.callback_query(F.data == 'settings')
async def settings(callback: types.CallbackQuery):
    await callback.answer()
    kb = InlineKeyboard.create_inline_kb(1, **list_settings, exit='🔚')
    await callback.message.edit_text('Настройки:', reply_markup=kb)


@userCallbackRout.callback_query(F.data == 'exit')
async def settings(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.delete()
    await callback.bot.delete_message(callback.message.chat.id, callback.message.message_id-1)


@userCallbackRout.callback_query(F.data == 'notifications')
async def notifications(callback: types.CallbackQuery):
    kb = InlineKeyboard.create_inline_kb(2, '🔙', **{SettingsCallbackData(category='notifications', choice=True).pack():'Да✅', SettingsCallbackData(category='notifications', choice=False).pack():'Нет❌'})
    await callback.answer(f'Лол что... ну ты и размечтался(-лась) конечно...\nТы, конечно, можешь поменять настройки, но толку...', show_alert=True)
    await callback.message.edit_text('Хотите ли вы получать уведомления?', reply_markup=kb)


@userCallbackRout.callback_query(F.data == 'day_block_messages')
async def day_block_messages(callback: types.CallbackQuery):
    kb = InlineKeyboard.create_inline_kb(2, '🔙', **{SettingsCallbackData(category='day_block_messages', choice=True).pack():'Да✅', SettingsCallbackData(category='day_block_messages', choice=False).pack():'Нет❌'})
    await callback.answer()
    await callback.message.edit_text('Хотите ли вы получать цельные сообщения для расписания на день?', reply_markup=kb)


@userCallbackRout.callback_query(F.data == 'week_block_messages')
async def week_block_messages(callback: types.CallbackQuery):
    kb = InlineKeyboard.create_inline_kb(2, '🔙', **{SettingsCallbackData(category='week_block_messages', choice=True).pack():'Да✅', SettingsCallbackData(category='week_block_messages', choice=False).pack():'Нет❌'})
    await callback.answer()
    await callback.message.edit_text('Хотите ли вы получать цельные сообщения для расписания на неделю?', reply_markup=kb)


@userCallbackRout.callback_query(SettingsCallbackData.filter())
async def choice_settings(callback: types.CallbackQuery, callback_data: SettingsCallbackData):
    try:
        set_settings(callback.from_user.id, callback_data.category, callback_data.choice)
        await callback.answer('👌')
    except:
        await callback.answer('Что-то пошло не так, воспользуйтесь командой /bagreport', show_alert=True)


@userCallbackRout.callback_query(ChangeSheduleCallbackData.filter((F.week == '') | (F.day == '')))
async def change_shedule(callback: types.CallbackQuery, callback_data: ChangeSheduleCallbackData):
    callback.answer()
    kb = None
    if callback_data.week == '':
        kb = InlineKeyboard.create_inline_kb(2, **{ChangeSheduleCallbackData(change=callback_data.change, week='current_week', day='').pack():'Текущая неделя', ChangeSheduleCallbackData(change=callback_data.change, week='next_week', day='').pack():'Следующая неделя'}, exit='🔚')
    elif callback_data.day == '':
        if callback_data.change == 'edit' or callback_data.change == 'delete':
            days = check_day(callback_data.week)
        if callback_data.change == 'add':
            days = check_day(callback_data.week, True)
        kb = InlineKeyboard.create_inline_kb(len(days), **{ChangeSheduleCallbackData(change=callback_data.change, week=callback_data.week, day=day).pack():day for day in days}, exit='🔚')
    else:
        pass

    await callback.message.edit_text('Редактирование расписания\nIn developing...', reply_markup=kb)


@userCallbackRout.callback_query(ChangeSheduleCallbackData.filter())
async def write_shedule(callback: types.CallbackQuery, callback_data: ChangeSheduleCallbackData):
    await callback.answer('Sorry 🥺')
    await callback.message.delete()
    await callback.bot.delete_message(callback.from_user.id, callback.message.message_id-1)

    