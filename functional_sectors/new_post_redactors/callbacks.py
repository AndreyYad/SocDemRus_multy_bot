from aiogram.types.callback_query import CallbackQuery
from aiogram.exceptions import TelegramBadRequest
from aiogram import F, Router

from .modules.database import set_like, remove_like, get_post_id_from_msg_id
from .modules.new_post import get_text_msg
from .modules.markups import markup_like
from .modules.messages import MESSAGES
from main_modules.bot_cmds import edit_msg_caption, edit_msg_text

router = Router()

async def callback_likes(call: CallbackQuery):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    msg_id = call.message.message_id
    
    match call.data:
        case '1_like':
            await set_like(user_id, msg_id)
            args_to_edit = (
                await get_text_msg(await get_post_id_from_msg_id(msg_id)),
                chat_id,
                msg_id,
                await markup_like()
            )
            
            try:
                edit_can = await edit_msg_caption(*args_to_edit)
            except TelegramBadRequest:
                edit_can = await edit_msg_text(*args_to_edit)
                
            if not edit_can:
                await call.answer(MESSAGES['not_edit_like'])
                
        case '1_remove_like':
            await remove_like(user_id, msg_id)
            args_to_edit = (
                await get_text_msg(await get_post_id_from_msg_id(msg_id)),
                chat_id,
                msg_id,
                await markup_like()
            )
            try:
                edit_can = await edit_msg_caption(*args_to_edit)
            except TelegramBadRequest:
                edit_can = await edit_msg_text(*args_to_edit)
                
            if not edit_can:
                await call.answer(MESSAGES['not_edit_removelike'])
                
def register_callbacks_new_post_redactors():
    router.callback_query.register(callback_likes, F.data.startswith('1_'))