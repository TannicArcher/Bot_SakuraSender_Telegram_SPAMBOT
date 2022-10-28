from datetime import datetime

from aiogram.types import Message, CallbackQuery

from keyboards.inline.menu import back_to_main_menu
from loader import dp, bot
from utils.db_api.db_commands import select_user


# ========================SHOW USER CABINET========================
from utils.other_utils import get_user_date


@dp.callback_query_handler(text="personal_acc")
async def personal_acc(call: CallbackQuery):
    bot_info = await bot.get_me()
    user = await select_user(call.from_user.id)
    result_date = await get_user_date(call.from_user.id)
    await call.message.edit_text(f"<b>#слито в @end_software 🖥 Профиль\n\n"
                                 f"🆔Ваш ID: <code>{call.from_user.id}</code>\n"
                                 f"📦Юзер добавленного аккаунта: <code>{user[1]}</code>\n"
                                 f"🧿Ваша подписка продлится еще:</b> "
                                 f"<code>{result_date}</code>",
                                 reply_markup=back_to_main_menu)
