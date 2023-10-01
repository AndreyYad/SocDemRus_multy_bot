from aiogram import types
from aiogram.dispatcher import FSMContext

from .bot_cmds import reply_msg
from .messages import MESSAGES
from .bot_dispatcher import dp
from .reset_state import reset
from .state_machine import FSMClient

@dp.message_handler(commands=['start'], state=None)
async def start_func(msg: types.Message):
    if msg.chat.type == 'private':
        await reply_msg(msg, MESSAGES['start'])

@dp.message_handler(commands=['cancel'], state='*')
async def cancel_func(msg: types.Message, state: FSMContext):
    await reset(msg, state)