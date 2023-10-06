'''Методы связаные с работой с базами данных'''

from aiosqlite import connect
from aiogram.dispatcher.storage import FSMContextProxy
from asyncio import run
import os

async def born_of_db():
    '''Создание таблиц'''
    try:
        os.mkdir('database')
    except FileExistsError:
        pass
    async with connect('database/msg_time.sql') as conn:
        cur = await conn.cursor()
        await cur.execute("CREATE TABLE IF NOT EXISTS msg (user_id int PRIMARY KEY, time_end_cd int)")
        await conn.commit()
    async with connect('database/new_post.sql') as conn:
        cur = await conn.cursor()
        await cur.execute("CREATE TABLE IF NOT EXISTS new_post (msg_id int PRIMARY KEY, user_id int, text_post text, headline_post varchar(200), picture_post bit)")
        await conn.commit()

async def set_end_cd(user_id: int, time_end_cd: int):
    '''Сохранение времени окончания коулдауна'''
    async with connect('database/msg_time.sql') as conn:
        cur = await conn.cursor()
        await cur.execute("INSERT OR IGNORE INTO msg (user_id) VALUES (?)", (user_id,))
        await cur.execute("UPDATE msg SET time_end_cd = ? WHERE user_id = ?", (time_end_cd, user_id))
        await conn.commit()

async def get_end_cd(user_id: int):
    '''Получение времени окончания коулдауна'''
    async with connect('database/msg_time.sql') as conn:
        cur = await conn.cursor()
        await cur.execute("SELECT time_end_cd FROM msg WHERE user_id = ?", (user_id,))
        try:
            result = (await cur.fetchall())[0][0]
        except IndexError:
            result = 0
    return result

async def save_new_post(msg_id: int, user_id: int, text: str, headline: str, picture: int):
    '''Сохранение данных о новом посте для оценки в редактуре'''
    async with connect('database/new_post.sql') as conn:
        cur = await conn.cursor()
        await cur.execute("INSERT OR IGNORE INTO new_post VALUES (?, ?, ?, ?, ?)", (msg_id, user_id, text, headline, picture))
        await conn.commit()

if __name__ == '__main__':
    print(run(born_of_db()))