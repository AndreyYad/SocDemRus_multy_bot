from main_modules.bot_cmds import send_msg, send_msg_photo, get_chat_member, get_inputfile
from main_modules.config import CHATS
from .messages import MESSAGES
from .database import get_post_data, set_msg_id_post
    
async def send_post_from_bd(post_id: int):
    
    user_id, text_post, headline_post, photo_post = await get_post_data(post_id)
    
    msg_text = MESSAGES['new_post_in_red'].format(
        user_id, 
        (await get_chat_member(user_id, CHATS['redactors']))['user']['first_name'],
        headline_post, 
        text_post
    )
    
    if photo_post == None:
        msg = await send_msg(
            CHATS['designers'], 
            msg_text
        )
    else:
        if photo_post:
            photo_msg = await get_inputfile(photo_post)
        else:
            photo_msg = open('images/defult.png', 'rb')
        msg = await send_msg_photo(
            CHATS['designers'], 
            photo_msg,
            msg_text
        )
        
    await set_msg_id_post(post_id, msg.message_id)