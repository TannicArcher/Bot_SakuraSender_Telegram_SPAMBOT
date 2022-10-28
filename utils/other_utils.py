import random
from datetime import datetime
import asyncio

import socks
from telethon.tl.functions.channels import JoinChannelRequest
from telethon import TelegramClient
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.types import InputChannel

from data.config import api_id, api_hash
from loader import scheduler
from utils.db_api.db_commands import select_user, select_user_proxy, select_user_accounts, update_messages_count


async def send_message_to_chat(user_id, chat_url, msg_txt, photo=None):
    proxies = await select_user_proxy(user_id)
    accounts = await select_user_accounts(user_id)
    for acc in accounts:
        try:
            if proxies:
                proxy_db = random.choice(proxies)[1].split(":")
                proxy = (socks.SOCKS5, proxy_db[1].split(":")[0], int(proxy_db[1].split(":")[1]),
                         proxy_db[0].split(":")[0], proxy_db[0].split(":")[1])
                proxy = (socks.SOCKS5, proxy_db[0], int(proxy_db[1]))
                client = TelegramClient(f"sessions/{acc[1]}", api_id, api_hash, proxy=proxy)
            else:
                client = TelegramClient(f"sessions/{acc[1]}", api_id, api_hash)
            await client.connect()
            if "joinchat" in chat_url:
                try:
                    await client(ImportChatInviteRequest(chat_url.split("/")[-1]))
                except Exception:
                    pass
            else:
                try:
                    await client(JoinChannelRequest(chat_url))
                except Exception:
                    pass
            if photo:
                await client.send_message(chat_url, msg_txt, file=photo, parse_mode="HTML")
            else:
                await client.send_message(chat_url, msg_txt, parse_mode="HTML")
            await update_messages_count()
            await client.disconnect()
        except Exception:
            await client.disconnect()


async def send_message_to_user(username, message_text, number):
    client = TelegramClient(f"sessions/{number}", api_id, api_hash)
    await client.connect()
    await client.send_message(username, message_text)
    await client.disconnect()
    await asyncio.sleep(2)


async def disconnect_client(number):
    client = TelegramClient(f"sessions/{number}", api_id, api_hash)
    await client.disconnect()


async def stop_job(user_id):
    job = scheduler.get_job(job_id=str(user_id))
    job.remove()


async def get_valid_date(user):
    date_list = user[3].split(" ")
    date_list = list(map(int, date_list))
    date_when_expired = datetime(date_list[0], date_list[1], date_list[2], date_list[3], date_list[4])
    return date_when_expired


async def get_user_date(user_id):
    user = await select_user(user_id)
    now_date = datetime.now()
    if user[3]:
        date_list = user[3].split(" ")
        date_list = list(map(int, date_list))
        date_when_expired = datetime(date_list[0], date_list[1], date_list[2], date_list[3], date_list[4])
        result_date = str(date_when_expired - now_date).split(".")[0].replace("days", "дня/дней").replace("day", "день")
    else:
        result_date = "00:00"

    return result_date
