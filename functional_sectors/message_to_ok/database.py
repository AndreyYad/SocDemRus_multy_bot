'''Методы связаные с работой с базами данных'''

from aiosqlite import connect
from sqlite3 import connect as connect_lite
from os import mkdir, path

path = path.abspath(__file__)[:path.abspath(__file__).rindex('\\')]

def create_database():
    '''Создание таблиц'''
    try:
        mkdir(path + '/database')
    except FileExistsError:
        pass
    with connect_lite(path + '/database/msg_time.sql') as conn:
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS msg (user_id int PRIMARY KEY, time_end_cd int)")
        conn.commit()

async def set_end_cd(user_id: int, time_end_cd: int):
    '''Сохранение времени окончания коулдауна'''
    async with connect(path + '/database/msg_time.sql') as conn:
        cur = await conn.cursor()
        await cur.execute("INSERT OR IGNORE INTO msg (user_id) VALUES (?)", (user_id,))
        await cur.execute("UPDATE msg SET time_end_cd = ? WHERE user_id = ?", (time_end_cd, user_id))
        await conn.commit()

async def get_end_cd(user_id: int):
    '''Получение времени окончания коулдауна'''
    async with connect(path + '/database/msg_time.sql') as conn:
        cur = await conn.cursor()
        await cur.execute("SELECT time_end_cd FROM msg WHERE user_id = ?", (user_id,))
        try:
            result = (await cur.fetchall())[0][0]
        except IndexError:
            result = 0
    return result