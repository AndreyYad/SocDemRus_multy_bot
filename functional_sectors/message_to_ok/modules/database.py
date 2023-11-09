'''Методы связаные с работой с базами данных'''

from aiosqlite import connect
from os import path

path = path.abspath(__file__)[:path.abspath(__file__).rindex('\\modules')]

async def set_end_cd(user_id: int, time_end_cd: int):
    '''Сохранение времени окончания коулдауна'''
    async with connect(path + '/database/db_msg_to_ok.sql') as conn:
        cur = await conn.cursor()
        await cur.execute("INSERT OR IGNORE INTO coulddawn (user_id) VALUES (?)", (user_id,))
        await cur.execute("UPDATE coulddawn SET time_end_cd = ? WHERE user_id = ?", (time_end_cd, user_id))
        await conn.commit()

async def get_end_cd(user_id: int):
    '''Получение времени окончания коулдауна'''
    async with connect(path + '/database/db_msg_to_ok.sql') as conn:
        cur = await conn.cursor()
        await cur.execute("SELECT time_end_cd FROM coulddawn WHERE user_id = ?", (user_id,))
        try:
            result = (await cur.fetchall())[0][0]
        except IndexError:
            result = 0
    return result

async def save_sent_message(msg_id: int, user_id: int):
    '''Сохранение информации об отправленном в ОК сообщении'''
    async with connect(path + '/database/db_msg_to_ok.sql') as conn:
        cur = await conn.cursor()
        await cur.execute("INSERT OR IGNORE INTO messages (msg_id, user_id) VALUES (?, ?)", (msg_id, user_id))
        await conn.commit()
        
async def get_author_id(msg_id: int):
    '''Получение айди пользователя по айди сообщения'''
    async with connect(path + '/database/db_msg_to_ok.sql') as conn:
        cur = await conn.cursor()
        await cur.execute("SELECT user_id FROM messages WHERE msg_id = ?", (msg_id,))
        try:
            result = (await cur.fetchall())[0][0]
        except IndexError:
            result = None
            print('z')
    return result