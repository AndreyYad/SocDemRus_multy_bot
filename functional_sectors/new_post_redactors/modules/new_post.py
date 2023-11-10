from aiogram import types
from aiogram.dispatcher.storage import FSMContextProxy

from main_modules.bot_cmds import send_msg, send_msg_photo
from main_modules.config import CHATS
from .messages import MESSAGES
from .database import save_new_post

async def new_post_to_red(user: types.user.User, data: FSMContextProxy):
    if data['new_post_text'] == 'нет':
        text = 'Пусто'
    else:
        text = data['new_post_text']

    if data['new_post_headline'] == 'нет':
        headline = 'Пусто'
    else:
        headline = data['new_post_headline']

    if data['new_post_picture'] == 'нет':
        photo = 0
    elif data['new_post_picture'] == 'не будет':
        photo = None
    else:
        photo = 1
        
    if photo == None:
        msg = await send_msg(
            CHATS['designers'], 
            MESSAGES['new_post_in_red'].format(
                user.id, 
                user.first_name,
                data['new_post_headline'], 
                data['new_post_text']
            )
        )
    else:
        if photo:
            photo_msg = data['new_post_picture']
        else:
            photo_msg = open('images/defult.png', 'rb')
        msg = await send_msg_photo(
            CHATS['designers'], 
            photo_msg,
            MESSAGES['new_post_in_red'].format(
                user.id, 
                user.first_name,
                data['new_post_headline'], 
                data['new_post_text']
            )
        )

    if headline == 'Пусто':
        headline = None
    if text == 'Пусто':
        text = None

    await save_new_post(msg.message_id, user.id, text, headline, photo)