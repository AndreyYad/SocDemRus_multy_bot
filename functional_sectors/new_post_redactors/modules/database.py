'''Методы связаные с работой с базами данных'''

from aiosqlite import connect
from aiogram.dispatcher.storage import FSMContextProxy
from os import path

path = path.abspath(__file__)[:path.abspath(__file__).rindex('\\modules')]

async def save_new_post(user_id: int, data: FSMContextProxy) -> int:
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
        await cur.execute("INSERT OR IGNORE INTO new_post (user_id, text_post, headline_post, picture_post) VALUES (?, ?, ?, ?)", (user_id, text, headline, photo))
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