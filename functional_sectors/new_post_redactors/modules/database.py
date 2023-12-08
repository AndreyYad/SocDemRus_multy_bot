'''Методы связаные с работой с базами данных'''

from aiosqlite import connect
from os import path
from time import time

path = path.abspath(__file__)[:path.abspath(__file__).rindex('\\modules')]

async def save_new_post(user_id: int, data) -> int:
    '''
    Сохранение данных о новом посте для оценки в редактуре
    
    Возвращение айди сохраняемого поста
    '''
    
    if data['new_post_text'] == 'нет':
        text = 'Пусто'
    else:
        text = data['new_post_text']

    if data['new_post_headline'] == 'нет':
        headline = 'Пусто'
    else:
        headline = data['new_post_headline']

    if data['new_post_picture'] == 'нет':
        photo = ''
    elif data['new_post_picture'] == 'не будет':
        photo = None
    else:
        photo = data['new_post_picture']
    
    async with connect(path + '/database/db_new_post.sql') as conn:
        cur = await conn.cursor()
        await cur.execute("INSERT OR IGNORE INTO new_post (user_id, text_post, headline_post, picture_post, time_repost) VALUES (?, ?, ?, ?, ?)", (user_id, text, headline, photo, int(time())+86400))
        await conn.commit()
        await cur.execute('SELECT COUNT(*) FROM new_post')
        post_id = (await cur.fetchall())[0][0]
        
    return post_id

async def set_msg_id_post(post_id: int, msg_id: int):
    '''Установка айди сообщения отправленого в чат редакторов с информацией о новом посте'''
    async with connect(path + '/database/db_new_post.sql') as conn:
        cur = await conn.cursor()
        await cur.execute("UPDATE new_post SET msg_id = ? WHERE post_id = ?", (msg_id, post_id))
        await conn.commit()
        
async def get_post_data(post_id: int) -> tuple:
    '''Получение данных поста по его айди в базе данных'''
    async with connect(path + '/database/db_new_post.sql') as conn:
        cur = await conn.cursor()
        await cur.execute("SELECT user_id, text_post, headline_post, picture_post FROM new_post WHERE post_id = ?", (post_id,))
        result = (await cur.fetchall())[0]
    return result

async def get_post_id_from_msg_id(msg_id: int):
    async with connect(path + '/database/db_new_post.sql') as conn:
        cur = await conn.cursor()
        await cur.execute("SELECT post_id FROM new_post WHERE msg_id = ?", (msg_id,))
        result = (await cur.fetchall())[0][0]
    return result

async def set_like(user_id: int, msg_id: int = None, post_id: int = None):
    if post_id is None:
        post_id = await get_post_id_from_msg_id(msg_id)
    async with connect(path + '/database/db_new_post.sql') as conn:
        cur = await conn.cursor()
        await cur.execute("SELECT * FROM likes")
        if (post_id, user_id) not in await cur.fetchall():
            await cur.execute("INSERT OR IGNORE INTO likes (post_id, user_id) VALUES (?, ?)", (post_id, user_id))
            await conn.commit()
            
async def remove_like(user_id: int, msg_id: int = None, post_id: int = None):
    if post_id is None:
        post_id = await get_post_id_from_msg_id(msg_id)
    async with connect(path + '/database/db_new_post.sql') as conn:
        cur = await conn.cursor()
        await cur.execute("DELETE FROM likes WHERE post_id = ? AND user_id = ?", (post_id, user_id))
        await conn.commit()
            
async def get_likers(msg_id: int = None, post_id: int = None):
    if post_id is None:
        post_id = await get_post_id_from_msg_id(msg_id)
    async with connect(path + '/database/db_new_post.sql') as conn:
        cur = await conn.cursor()
        await cur.execute("SELECT user_id FROM likes WHERE post_id = ?", (post_id,))
        result = [user_id[0] for user_id in await cur.fetchall()]
    return result