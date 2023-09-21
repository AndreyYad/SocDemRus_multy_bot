from aiogram import types

from modules.config import DEBUG
from modules.bot_dispatcher import dp

# commands=['id']
async def get_id_func(msg: types.Message):
    if DEBUG:
        print('{}: {}'.format(msg.chat.full_name, msg.chat.id))

def register_handlers():
    dp.register_message_handler(get_id_func, commands=['id'])