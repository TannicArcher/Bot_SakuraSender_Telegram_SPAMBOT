from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import CallbackQuery
from proxy_checker import ProxyChecker
from telethon import TelegramClient

from data.config import ADMINS, api_id, api_hash
from filters import IsNotSubscribed
from keyboards.inline.menu import admin_menu, main_menu, back_to_main_menu
from loader import dp
from utils.db_api.db_commands import *
from utils.other_utils import get_user_date, send_message_to_chat


@dp.callback_query_handler(IsNotSubscribed())
async def answer_call(call: CallbackQuery):
    await call.answer("❗️У вас нету подписки, чтобы пользоваться ботом")


# ========================DELETE BROADCAST MESSAGE========================
# WITH STATE
@dp.callback_query_handler(text="delete_this_message", state="*")
async def del_broadcast_msg(call: CallbackQuery):
    await call.message.delete()


# ========================SHOW MAIN MENU========================
# /start WITHOUT STATE
@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    if not await select_user(message.from_user.id):
        await add_user(message.from_user.id)
    stat, user = await select_statistic(), await select_user(message.from_user.id)
    result_date = await get_user_date(message.from_user.id)
    proxy = await select_user_proxy(message.from_user.id)
    await message.answer(text=f"<b> #слито в @end_software 🤖Аккаунтов добавлено: {stat[0]}\n"
                              f"☢️Сделано атак: {stat[1]}\n\n"
                              f"✉️Отправлено сообщений: {stat[2]}\n"
                              f"🧬Прокси: {'✔️Есть' if proxy else '❗️Нету'}\n"
                              f"🔓Подписка активна: {result_date}\n"
                              f"♻️Выходить после спама: {'✅' if user[6] == 1 else '⛔️'}</b>",
                         reply_markup=await main_menu(message.from_user.id))


@dp.callback_query_handler(text="back_to_main_menu", state="*")
async def support(call: CallbackQuery, state: FSMContext):
    await state.finish()
    user = await select_user(call.from_user.id)
    stat, proxy = await select_statistic(), await select_user_proxy(call.from_user.id)
    result_date = await get_user_date(call.from_user.id)
    if not call.message.photo:
        await call.message.edit_text(text=f"<b>🤖Аккаунтов добавлено: {stat[0]}\n"
                                          f"☢️Сделано атак: {stat[1]}\n\n"
                                          f"✉️Отправлено сообщений: {stat[2]}\n"
                                          f"🧬Прокси: {'✔️Есть' if proxy else '❗️Нету'}\n"
                                          f"🔓Подписка активна: {result_date}\n"
                                          f"♻️Выходить после спама: {'✅' if user[6] == 1 else '⛔️'}</b>",
                                     reply_markup=await main_menu(call.from_user.id))
    else:
        await call.message.delete()
        await call.message.answer(text=f"<b>🤖Аккаунтов добавлено: {stat[0]}\n"
                                       f"☢️Сделано атак: {stat[1]}\n\n"
                                       f"✉️Отправлено сообщений: {stat[2]}\n"
                                       f"🧬Прокси: {'✔️Есть' if proxy else '❗️Нету'}\n"
                                       f"🔓Подписка активна: {result_date}\n"
                                       f"♻️Выходить после спама: {'✅' if user[6] == 1 else '⛔️'}</b>",
                                  reply_markup=await main_menu(call.from_user.id))


# BACK FROM ANY HANDLER TO MAIN MENU WITH STATE
@dp.callback_query_handler(text="back_admin", state="*")
async def support(call: CallbackQuery, state: FSMContext):
    await state.finish()
    if str(call.from_user.id) in ADMINS:
        await call.message.edit_text("Админ-меню", reply_markup=admin_menu)


# ========================INFO BUTTON========================
@dp.callback_query_handler(text="inf")
async def support(call: CallbackQuery):
    await call.message.edit_text(
        "<b>👋 Привет, данный бот создан для удобного авто~постинга во все чаты телеграмма!\n\n"
        "♻️ Отправлять любому юзеру своё сообщение от добавленного аккаунта!\n"
        "♻️ Добавлять хоть 100 чатов (и настраивать их одновременно)\n"
        "♻️Включать / отключать рассылки.\n"
        "♻️Менять все параметры, задержки / текст / фото / и другие!\n\n"
        "🚀Удачного использования!</b>",
        reply_markup=back_to_main_menu)
