from loguru import logger

from main_modules.bot_cmds import send_msg, send_msg_photo, get_inputfile, get_name_user, edit_msg_any
from main_modules.config import CHATS, ID_EMPTY_PICTURE
from .messages import MESSAGES
from .database import get_post_data, set_msg_id_post, get_likers, get_msg_id_from_post_id, delete_post_in_bd
from .markups import markup_like
    
async def get_text_msg(post_id: int, type: int=1, **kwargs):
    '''
    Получение текста для сообщения с информацией о новом посте
    
    type=1 - текст с лайками
    
    type=2 - текст не актуального сообщения (укажите ссылку на новое сообщение как msg_url)
    
    type=3 - текст удаленого поста
    
    type=4 - текст поста отправленного дизайнерам
    '''
    
    user_id, text_post, headline_post = (await get_post_data(post_id))[:3]
    
    msg_text = MESSAGES['new_post_in_red'].format(
        user_id, 
        await get_name_user(user_id),
        headline_post, 
        text_post
    )
    
    match type:
        case 1:
            if await get_likers(post_id=post_id):
                msg_text += '\nСписок лайкнувших:' + ''.join(
                    [
                        '\n<a href="tg://user?id={}">{}</a>'.format(
                            user_id,
                            await get_name_user(user_id)
                        ) 
                        for user_id in await get_likers(post_id=post_id)
                    ]
                )
            else:
                msg_text += '\n<i>Лайков пока нет</i>'
        case 2:
            msg_text += MESSAGES['link_repost'].format(kwargs['msg_url'])
        case 3:
            msg_text += MESSAGES['delete_text']
        case 4:
            msg_text += MESSAGES['send_post_text']
        
    return msg_text
    
async def send_post_from_bd(post_id: int):
    
    msg_text = await get_text_msg(post_id)
    
    photo_post = (await get_post_data(post_id))[3]
    
    if photo_post == None:
        msg = await send_msg(
            CHATS['redactors'], 
            msg_text, 
            await markup_like()
        )
    else:
        msg = await send_msg_photo(
            CHATS['redactors'], 
            await get_inputfile(photo_post),
            msg_text,
            await markup_like()
        )
        
    await set_msg_id_post(post_id, msg.message_id)
    
    return msg

async def send_to_design(post_id: int):
    post_data = await get_post_data(post_id)
    text = post_data[1]
    headline = post_data[2]
    photo = post_data[3]
    if len(await get_likers(post_id=post_id)) >= 4 and 'Пусто' not in [text, headline] and (photo != ID_EMPTY_PICTURE or photo == None):
        await edit_msg_any(
            await get_text_msg(post_id, type=4), 
            CHATS['redactors'], 
            await get_msg_id_from_post_id(post_id)
        )
        if photo == None:
            await send_msg(
                CHATS['designers'],
                await get_text_msg(post_id, type=0)
            )
        else:
            await send_msg_photo(
                CHATS['designers'],
                await get_inputfile(photo),
                await get_text_msg(post_id, type=0)
            )
        await delete_post_in_bd(post_id)