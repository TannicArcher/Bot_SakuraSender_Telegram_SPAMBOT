import logging

from aiogram import Dispatcher

from data.config import ADMINS
from keyboards.inline.menu import broadcast_menu


async def on_startup_notify(dp: Dispatcher):
    for admin in ADMINS:
        try:
            await dp.bot.send_message(admin, "Бот Запущен #слито в @end_software", reply_markup=broadcast_menu)

        except Exception as err:
            logging.exception(err)
