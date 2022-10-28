import aiosqlite


# ========================USERS========================
async def add_user(user_id):
    conn = await aiosqlite.connect('db.db', check_same_thread=False)
    await conn.execute("INSERT INTO users (user_id) VALUES(?)", (user_id,))
    await conn.commit()
    await conn.close()


async def add_proxy(user_id, proxy):
    conn = await aiosqlite.connect('db.db', check_same_thread=False)
    await conn.execute("INSERT INTO proxies(user_id, proxy) VALUES(?,?)", (user_id, proxy))
    await conn.commit()
    await conn.close()


async def del_proxy(user_id, proxy):
    conn = await aiosqlite.connect('db.db', check_same_thread=False)
    await conn.execute("DELETE FROM proxies WHERE user_id=? AND proxy=?", (user_id, proxy))
    await conn.commit()
    await conn.close()


async def select_user_proxy(user_id):
    conn = await aiosqlite.connect('db.db', check_same_thread=False)
    cursor = await conn.execute(f"SELECT * FROM proxies WHERE user_id=?", (user_id,))
    h = await cursor.fetchall()
    await conn.close()
    return h


async def select_proxy(user_id, proxy):
    conn = await aiosqlite.connect('db.db', check_same_thread=False)
    cursor = await conn.execute(f"SELECT * FROM proxies WHERE user_id=? AND proxy=?", (user_id, proxy))
    h = await cursor.fetchone()
    await conn.close()
    return h


async def select_all_users():
    conn = await aiosqlite.connect('db.db', check_same_thread=False)
    cursor = await conn.execute(f"SELECT * FROM users")
    h = await cursor.fetchall()
    await conn.close()
    return h


async def select_user(user_id):
    conn = await aiosqlite.connect('db.db', check_same_thread=False)
    cursor = await conn.execute(f"SELECT * FROM users WHERE user_id=?", (user_id,))
    h = await cursor.fetchone()
    await conn.close()
    return h


async def update_date(user_id, date):
    conn = await aiosqlite.connect('db.db', check_same_thread=False)
    await conn.execute("UPDATE users SET access_expired=? WHERE user_id=?", (date, user_id))
    await conn.commit()
    await conn.close()


async def update_session(user_id, session):
    conn = await aiosqlite.connect('db.db', check_same_thread=False)
    await conn.execute("UPDATE users SET telethon_session=? WHERE user_id=?", (session, user_id))
    await conn.commit()
    await conn.close()


async def del_user(user_id):
    conn = await aiosqlite.connect('db.db', check_same_thread=False)
    await conn.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
    await conn.commit()
    await conn.close()


async def add_acc(user_id, number):
    conn = await aiosqlite.connect('db.db', check_same_thread=False)
    await conn.execute("INSERT INTO accounts (user_id, account_num) VALUES(?,?)",
                       (user_id, number))
    await conn.commit()
    await conn.close()


async def del_acc(user_id, number):
    conn = await aiosqlite.connect('db.db', check_same_thread=False)
    await conn.execute("DELETE FROM accounts WHERE user_id=? AND account_num=?",
                       (user_id, number))
    await conn.commit()
    await conn.close()


async def get_acc_num(user_id, num):
    conn = await aiosqlite.connect('db.db', check_same_thread=False)
    cursor = await conn.execute(f"SELECT * FROM accounts WHERE user_id=? AND account_num=?", (user_id, num))
    h = await cursor.fetchall()
    await conn.close()
    return h


async def select_user_accounts(user_id):
    conn = await aiosqlite.connect('db.db', check_same_thread=False)
    cursor = await conn.execute(f"SELECT * FROM accounts WHERE user_id=?", (user_id,))
    h = await cursor.fetchall()
    await conn.close()
    return h


async def update_leave(user_id, num):
    conn = await aiosqlite.connect('db.db', check_same_thread=False)
    await conn.execute("UPDATE users SET leave=? WHERE user_id=?",
                       (num, user_id))
    await conn.commit()
    await conn.close()


# ======================STAT===================
async def select_statistic():
    conn = await aiosqlite.connect('db.db', check_same_thread=False)
    cursor = await conn.execute(f"SELECT * FROM stat")
    h = await cursor.fetchone()
    await conn.close()
    return h


async def update_acc_count():
    conn = await aiosqlite.connect('db.db', check_same_thread=False)
    await conn.execute("UPDATE stat SET accounts_count=accounts_count + 1")
    await conn.commit()
    await conn.close()


async def update_attacks():
    conn = await aiosqlite.connect('db.db', check_same_thread=False)
    await conn.execute("UPDATE stat SET attacks=attacks + 1")
    await conn.commit()
    await conn.close()


async def update_messages_count():
    conn = await aiosqlite.connect('db.db', check_same_thread=False)
    await conn.execute("UPDATE stat SET messages_count=messages_count + 1")
    await conn.commit()
    await conn.close()
