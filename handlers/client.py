from aiogram import types, Dispatcher

from modules.bot_cmds import *
from modules.messages import MESSAGES
from modules.bot_dispatcher import dp

# @dp.message_handler(commands=['start'])
async def start_func(msg: types.Message):
    if msg.chat.type == 'private':
        await send_msg(msg.from_user.id, MESSAGES['start'])

def register_handlers_client():
    dp.register_message_handler(start_func, commands=['start'])