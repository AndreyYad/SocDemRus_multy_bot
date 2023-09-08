from aiogram import types
from aiogram.dispatcher.storage import FSMContextProxy

from modules import sql_cmds
from modules.bot_cmds import *
from modules.config import CHATS, COULDDAWN_ANONIM_MSG
from modules.messages import MESSAGES
from modules.bot_dispatcher import dp

async def send_anonim_msg(msg: types.Message):
    user_id = msg.from_user.id
    msg_time = msg.date.timestamp()
    if await check_user_in_chat(user_id, CHATS['work']):
        cd = await sql_cmds.get_end_cd(user_id) - msg_time
        if cd <= 0:
            await sql_cmds.set_end_cd(user_id, msg_time + COULDDAWN_ANONIM_MSG)
            for chat_id in [CHATS['org_com'], CHATS['test_anon']][int(msg.text.startswith('test//')):]:
                await send_msg(chat_id, msg.text)
            return 'Сообщение отправлено в "{}"!'.format(await get_chat_name(CHATS['org_com']))
        else:
            return 'Ещё один запрос сможете отправить только через {}'.format(await _get_coulddawn_text(cd))
    else:
        return 'Вы не состоите в "{}"!'.format(await get_chat_name(CHATS['work']))
    
async def ban_in_all_chats(user_id: int):
    for chat_id in CHATS.values():
        if await check_user_in_chat(user_id, chat_id):
            await dp.bot.ban_chat_member(chat_id, user_id)
            await dp.bot.unban_chat_member(chat_id, user_id)

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

    await sql_cmds.save_new_post(msg.message_id, user.id, text, headline, photo)

    
async def _get_coulddawn_text(coulddawn: int):
    '''Текст об окончании кулдауна'''
    if coulddawn > 59:
        result = '{} мин.'.format(int(coulddawn // 60))
    else:
        result = '{} сек.'.format(int(coulddawn))
    return result