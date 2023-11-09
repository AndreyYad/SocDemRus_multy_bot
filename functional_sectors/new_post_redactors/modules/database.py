'''Методы связаные с работой с базами данных'''

from aiosqlite import connect
from os import path

path = path.abspath(__file__)[:path.abspath(__file__).rindex('\\modules')]

async def save_new_post(msg_id: int, user_id: int, text: str, headline: str, picture: int):
    '''Сохранение данных о новом посте для оценки в редактуре'''
    async with connect('database/new_post.sql') as conn:
        cur = await conn.cursor()
        await cur.execute("INSERT OR IGNORE INTO new_post VALUES (?, ?, ?, ?, ?)", (msg_id, user_id, text, headline, picture))
        await conn.commit()