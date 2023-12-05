from main_modules.bot_cmds import send_msg, send_msg_photo, get_inputfile, get_name_user
from main_modules.config import CHATS
from .messages import MESSAGES
from .database import get_post_data, set_msg_id_post, get_likers
from .markups import markup_like
    
async def get_text_msg(post_id: int):
    
    user_id, text_post, headline_post = (await get_post_data(post_id))[:3]
    
    msg_text = MESSAGES['new_post_in_red'].format(
        user_id, 
        await get_name_user(user_id),
        headline_post, 
        text_post
    )
    
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
        
    return msg_text
    
async def send_post_from_bd(post_id: int):
    
    msg_text = await get_text_msg(post_id)
    
    photo_post = (await get_post_data(post_id))[3]
    
    if photo_post == None:
        msg = await send_msg(
            CHATS['designers'], 
            msg_text, 
            await markup_like()
        )
    else:
        if photo_post:
            photo_msg = await get_inputfile(photo_post)
        else:
            photo_msg = open('images/defult.png', 'rb')
        msg = await send_msg_photo(
            CHATS['designers'], 
            photo_msg,
            msg_text,
            await markup_like()
        )
        
    await set_msg_id_post(post_id, msg.message_id)