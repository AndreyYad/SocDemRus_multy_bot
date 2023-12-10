'''Методы связаные с работой с базами данных'''

from aiosqlite import connect
from os import path
from time import time

from main_modules.config import TIME_FOR_REPOST, ID_EMPTY_PICTURE

path = path.abspath(__file__)[:path.abspath(__file__).rindex('modules')-1]

get_time_repost = lambda: int(time())+TIME_FOR_REPOST

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
        photo = ID_EMPTY_PICTURE
    elif data['new_post_picture'] == 'не будет':
        photo = None
    else:
        photo = data['new_post_picture']
    
    async with connect(path + '/database/db_new_post.sql') as conn:
        cur = await conn.cursor()
        await cur.execute(
            "INSERT OR IGNORE INTO new_post (user_id, text_post, headline_post, picture_post, time_repost) VALUES (?, ?, ?, ?, ?)", 
            (user_id, text, headline, photo, get_time_repost())
        )
        await conn.commit()
        await cur.execute('SELECT post_id FROM new_post')
        post_id = max([post_id[0] for post_id in await cur.fetchall()])
        
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
        await cur.execute("SELECT user_id, text_post, headline_post, picture_post, time_repost FROM new_post WHERE post_id = ?", (post_id,))
        result = (await cur.fetchall())[0]
    return result

async def get_post_id_from_msg_id(msg_id: int):
    '''Получение айди поста по айди его сообщения'''
    async with connect(path + '/database/db_new_post.sql') as conn:
        cur = await conn.cursor()
        await cur.execute("SELECT post_id FROM new_post WHERE msg_id = ?", (msg_id,))
        result = await cur.fetchall()
        if len(result) == 0:
            result = None
        else:
            result = result[0][0]
    return result

async def get_msg_id_from_post_id(post_id: int):
    '''Получение айди сообщения по айди его поста'''
    async with connect(path + '/database/db_new_post.sql') as conn:
        cur = await conn.cursor()
        await cur.execute("SELECT msg_id FROM new_post WHERE post_id = ?", (post_id,))
        result = await cur.fetchall()
        if len(result) == 0:
            result = None
        else:
            result = result[0][0]
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

async def add_time_repost(post_id: int):
    '''Добавление времени репоста'''
    async with connect(path + '/database/db_new_post.sql') as conn:
        cur = await conn.cursor()
        await cur.execute("UPDATE new_post SET time_repost = ? WHERE post_id = ?", (get_time_repost(), post_id))
        await conn.commit()
        
async def get_posts_id():
    '''Получение списка всех айди постов'''
    async with connect(path + '/database/db_new_post.sql') as conn:
        cur = await conn.cursor()
        await cur.execute("SELECT post_id FROM new_post")
        return [post_id[0] for post_id in await cur.fetchall()]
    
async def get_msgs_id():
    '''Получение списка всех айди постов'''
    async with connect(path + '/database/db_new_post.sql') as conn:
        cur = await conn.cursor()
        await cur.execute("SELECT msg_id FROM new_post")
        return [msg_id[0] for msg_id in await cur.fetchall()]
    
async def change_post_data(post_id: int, type_data: str, new_data: str):
    '''Смена данных предложенного поста'''
    async with connect(path + '/database/db_new_post.sql') as conn:
        cur = await conn.cursor()
        await cur.execute(f"UPDATE new_post SET {type_data}_post = ? WHERE post_id = ?", (new_data, post_id))
        await conn.commit()
        
async def get_author(msg_id: int = None, post_id: int = None):
    if post_id is None:
        post_id = await get_post_id_from_msg_id(msg_id)
    async with connect(path + '/database/db_new_post.sql') as conn:
        cur = await conn.cursor()
        await cur.execute("SELECT user_id FROM new_post WHERE post_id = ?", (post_id,))
        result = await cur.fetchall()
        if len(result) == 1:
            result = result[0][0]
        else:
            result = None
    return result

async def delete_post_in_bd(post_id: int):
    async with connect(path + '/database/db_new_post.sql') as conn:
        cur = await conn.cursor()
        await cur.execute("DELETE FROM new_post WHERE post_id = ?", (post_id,))
        await cur.execute("DELETE FROM likes WHERE post_id = ?", (post_id,))
        await conn.commit()