from aiogram.types.callback_query import CallbackQuery
from aiogram import F, Router

from .modules.database import set_like, remove_like, get_post_id_from_msg_id, get_author
from .modules.new_post import get_text_msg, send_to_design
from .modules.markups import markup_like
from .modules.messages import MESSAGES
from main_modules.bot_cmds import edit_msg_caption, edit_msg_text

router = Router()

async def callback_likes(call: CallbackQuery):
    liking = call.data == '1_like'
            
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    msg_id = call.message.message_id
    post_id = await get_post_id_from_msg_id(msg_id)
    with_photo = call.message.photo != None
    
    print(await get_author(post_id=post_id))
    
    if (user_id == await get_author(post_id=post_id)) and liking:
        await call.answer('Нельзя ставить лайк своему посту!')
        return
    
    if liking:
        await set_like(user_id, msg_id)
    else:
        await remove_like(user_id, msg_id)
    args_to_edit = (
        await get_text_msg(post_id),
        chat_id,
        msg_id,
        await markup_like()
    )

    if with_photo:
        edit_can = await edit_msg_caption(*args_to_edit)
    else:
        edit_can = await edit_msg_text(*args_to_edit)
        
    if liking:
        answer_text = MESSAGES['not_edit_like']
    else:
        answer_text = MESSAGES['not_edit_removelike']
        
    if not edit_can:
        await call.answer(answer_text)
        
    await send_to_design(post_id)
                
async def register_callbacks_new_post_redactors():
    router.callback_query.register(callback_likes, F.data.startswith('1_'))