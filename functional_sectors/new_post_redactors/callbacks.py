from aiogram.types.callback_query import CallbackQuery
from aiogram.utils.exceptions import BadRequest

from .modules.database import set_like, remove_like, get_post_id_from_msg_id
from .modules.new_post import get_text_msg
from .modules.markups import markup_like
from main_modules.bot_cmds import edit_msg_caption, edit_msg_text

async def callback(call: CallbackQuery):
    
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    msg_id = call.message.message_id
    
    match call.data:
        case 'like':
            await set_like(user_id, msg_id)
            args_to_edit = (
                await get_text_msg(await get_post_id_from_msg_id(msg_id)),
                chat_id,
                msg_id,
                await markup_like()
            )
            try:
                await edit_msg_caption(*args_to_edit)
            except BadRequest:
                await edit_msg_text(*args_to_edit)
        case 'remove_like':
            await remove_like(user_id, msg_id)
            args_to_edit = (
                await get_text_msg(await get_post_id_from_msg_id(msg_id)),
                chat_id,
                msg_id,
                await markup_like()
            )
            try:
                await edit_msg_caption(*args_to_edit)
            except BadRequest:
                await edit_msg_text(*args_to_edit)