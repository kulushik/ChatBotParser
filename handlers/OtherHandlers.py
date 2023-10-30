from aiogram import types, Router, F
from aiogram.filters import JOIN_TRANSITION, ChatMemberUpdatedFilter
from logic.Setting import register, unregister
import tzlocal


otherRout = Router()


@otherRout.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=JOIN_TRANSITION))
async def join(event: types.ChatMemberUpdated):
    user = event.from_user
    date = event.date.astimezone(tzlocal.get_localzone()).strftime('%d.%m.%Y %H:%M:%S')
    register(user.id, user.full_name, user.username, date)


@otherRout.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=~JOIN_TRANSITION))
async def join(event: types.ChatMemberUpdated):
    date = event.date.astimezone(tzlocal.get_localzone()).strftime('%d.%m.%Y %H:%M:%S')
    unregister(event.from_user.id, date)
