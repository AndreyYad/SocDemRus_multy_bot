from aiogram.types.callback_query import CallbackQuery
from aiogram import F, Router

from .modules.messages import MESSAGES
from .modules.send_post import send_post
from .modules.json_data import set_send_status
from main_modules.bot_cmds import edit_msg_text
from main_modules.config import CHANNEL

router = Router()

async def callback_send_now(call: CallbackQuery):
    await set_send_status(True)
    await send_post(call.message)

async def callback_cancel_send(call: CallbackQuery):
    await set_send_status(True)
    chat_id = call.message.chat.id
    msg_id = call.message.message_id
    await edit_msg_text(MESSAGES['cancel_send'], chat_id, msg_id)
                
async def register_callbacks_repost_from_vk():
    router.callback_query.register(callback_send_now, F.data == '2_send_now')
    router.callback_query.register(callback_cancel_send, F.data == '2_cancel_send')