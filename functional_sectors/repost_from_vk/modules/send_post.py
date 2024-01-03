from aiogram import types

from .messages import MESSAGES
from main_modules.bot_cmds import forward_msg, edit_msg_text
from main_modules.config import CHANNEL

async def send_post(reply_msg: types.Message):
    chat_id = reply_msg.chat.id
    msg_id = reply_msg.message_id
    post_msg_id = reply_msg.reply_to_message.message_id
    await forward_msg(CHANNEL, chat_id, post_msg_id, anonim=True)
    await edit_msg_text(MESSAGES['sent'], chat_id, msg_id)