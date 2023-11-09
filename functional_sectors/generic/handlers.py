from aiogram import types
from aiogram.dispatcher import FSMContext

from .bot_cmds import reply_msg, get_chat_name
from .messages import MESSAGES
from .config import DEVELOPERS
from .bot_dispatcher import dp
from .reset_state import reset

@dp.message_handler(commands=['start'], state=None)
async def start_func(msg: types.Message):
    if msg.chat.type == 'private':
        await reply_msg(msg, MESSAGES['start'])

@dp.message_handler(commands=['cancel'], state='*')
async def cancel_func(msg: types.Message, state: FSMContext):
    await reset(msg, state)
    
@dp.message_handler(regexp='\A!name -\d+\Z', state=None)
async def name_chat(msg: types.Message):
    if msg.chat.id in DEVELOPERS:
        await reply_msg(msg, await get_chat_name(int(msg.text[6:])))