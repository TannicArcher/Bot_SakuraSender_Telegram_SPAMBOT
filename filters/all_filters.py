import re
from datetime import datetime

from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from data.config import ADMINS
from utils.db_api.db_commands import select_user
from utils.other_utils import get_valid_date


class IsPrivate(BoundFilter):
    async def check(self, message: types.Message):
        return message.chat.type == types.ChatType.PRIVATE


class IsSubscribed(BoundFilter):
    async def check(self, call: types.CallbackQuery):
        user = await select_user(call.from_user.id)
        if user[3]:
            date_when_expired = await get_valid_date(user)
            if datetime.now() < date_when_expired:
                return True


class IsNotSubscribed(BoundFilter):
    async def check(self, call: types.CallbackQuery):
        user = await select_user(call.from_user.id)
        if user:
            if str(call.from_user.id) not in ADMINS:
                if not user[3]:
                    return True
                else:
                    date_when_expired = await get_valid_date(user)
                    if datetime.now() > date_when_expired:
                        return True
