import asyncio
import os
import random
from datetime import datetime, timedelta

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.exceptions import Unauthorized

from keyboards.inline.menu import back_admin, admin_menu, choose_menu
from loader import dp, bot
from states.states import BroadcastState, GiveTime, TakeTime
from utils.db_api.db_commands import select_all_users, del_user, update_date


@dp.callback_query_handler(text="give_time")
async def edit_commission(call: CallbackQuery, state: FSMContext):
    msg_to_edit = await call.message.edit_text("<b>🆔Введите ID человека:</b>",
                                               reply_markup=back_admin)
    await GiveTime.GT1.set()
    await state.update_data(msg_to_edit=msg_to_edit)


@dp.message_handler(state=GiveTime.GT1)
async def receive_com(message: Message, state: FSMContext):
    data = await state.get_data()
    msg_to_edit = data.get("msg_to_edit")
    user_id = message.text
    await message.delete()
    await GiveTime.next()
    await state.update_data(user_id=user_id)
    await msg_to_edit.edit_text("<b>⏰Введите время в часах которое выдать человеку:</b>", reply_markup=back_admin)


@dp.message_handler(state=GiveTime.GT2)
async def receive_com(message: Message, state: FSMContext):
    data = await state.get_data()
    msg_to_edit, user_id = data.get("msg_to_edit"), data.get("user_id")
    try:
        hours = int(message.text)
        await message.delete()
        date_when_expires = datetime.now() + timedelta(hours=hours)
        date_to_db = str(date_when_expires).split(".")[0].replace("-", " ").split(":")
        date_to_db = " ".join(date_to_db[:-1])
        await update_date(user_id, date_to_db)
        await state.finish()
        await msg_to_edit.edit_text("<b>Доступ выдан.</b>", reply_markup=back_admin)
    except ValueError:
        await msg_to_edit.edit_text("<b>⏰Не верный формат, попробуйте еще раз.</b>")


@dp.callback_query_handler(text="take_time")
async def edit_commission(call: CallbackQuery, state: FSMContext):
    msg_to_edit = await call.message.edit_text("<b>🆔Введите ID человека:</b>",
                                               reply_markup=back_admin)
    await TakeTime.T1.set()
    await state.update_data(msg_to_edit=msg_to_edit)


@dp.message_handler(state=TakeTime.T1)
async def receive_com(message: Message, state: FSMContext):
    data = await state.get_data()
    msg_to_edit = data.get("msg_to_edit")
    user_id = message.text
    await message.delete()
    await update_date(user_id, None)
    await state.finish()
    await msg_to_edit.edit_text("<b>У юзера больше нет доступа.</b>", reply_markup=back_admin)


# ========================BROADCAST========================
# ASK FOR PHOTO AND TEXT
@dp.callback_query_handler(text="broadcast")
async def broadcast2(call: CallbackQuery):
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    await call.message.answer("<b>Отправь фото с текстом, которые будут рассылаться по юзерам\n"
                              "Можно просто текст</b>", reply_markup=back_admin)
    await BroadcastState.BS1.set()


# RECEIVE PHOTO OR TEXT
@dp.message_handler(content_types=['photo', 'text'], state=BroadcastState.BS1)
async def broadcast4(message: Message, state: FSMContext):
    await message.delete()
    if message.photo:
        easy_chars = 'abcdefghijklnopqrstuvwxyz1234567890'
        name = ''
        for i in range(10):
            name += random.choice(easy_chars)
        photo_name = name + ".jpg"
        await message.photo[-1].download(f"pics/broadcast/{photo_name}")
        await state.update_data(photo=photo_name, text=message.caption)
        await asyncio.sleep(2)
        path = f'pics/broadcast/{photo_name}'
        with open(path, 'rb') as f:
            photo = f.read()
        await message.answer_photo(photo=photo, caption=f"{message.caption}\n\n"
                                                        f"<b>Все правильно? Отправляем?</b>",
                                   reply_markup=choose_menu)
    else:
        await state.update_data(text=message.text)
        await message.answer(message.text + "\n\n<b>Все правильно? Отправляем?</b>", reply_markup=choose_menu)
    await BroadcastState.next()


# START BROADCAST
@dp.callback_query_handler(text="broadcast:yes", state=BroadcastState.BS2)
async def broadcast_text_post(call: CallbackQuery, state: FSMContext):
    users = await select_all_users()
    data = await state.get_data()
    text, photo_name = data.get("text"), data.get('photo')
    await state.finish()
    msg_to_delete = await call.message.answer("<b>Рассылка начата</b>")
    if photo_name is None:
        for user in users:
            try:
                await bot.send_message(user[0], text)
            except Unauthorized:
                await del_user(user[0])
    else:
        path = f'pics/broadcast/{photo_name}'
        with open(path, 'rb') as f:
            photo = f.read()
        for user in users:
            try:
                await bot.send_photo(chat_id=user[0], photo=photo, caption=text)
            except Unauthorized:
                await del_user(user[0])
        os.remove(path)
    await msg_to_delete.delete()
    await call.message.answer("<b>Рассылка закончена</b>", reply_markup=back_admin)


# CANCEL BROADCAST
@dp.callback_query_handler(text="broadcast:no", state=BroadcastState.BS2)
async def broadcast_text_post(call: CallbackQuery, state: FSMContext):
    if not call.message.photo:
        await call.message.edit_text("<b>Админ-меню</b>", reply_markup=admin_menu)
    else:
        await call.message.delete()
        await call.message.answer("<b>Админ-меню</b>", reply_markup=admin_menu)
    await state.finish()
