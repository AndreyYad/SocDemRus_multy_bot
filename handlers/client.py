from aiogram import types
from aiogram.dispatcher import FSMContext

from modules.bot_cmds import reply_msg
from modules.messages import MESSAGES
from modules.bot_dispatcher import dp

async def _reset(msg: types.Message, state: FSMContext):
    '''Сброс состояния'''
    async with state.proxy() as data:
        if data.state != None:
            await state.finish()
            await reply_msg(msg, MESSAGES['reset'])

# commands=['start']
async def start_func(msg: types.Message):
    if msg.chat.type == 'private':
        await reply_msg(msg, MESSAGES['start'])
        print(msg.from_user.first_name)

# Сброс состояния
# commands=['cancel']
async def cancel_func(msg: types.Message, state: FSMContext):
    await _reset(msg, state)

def register_handlers():
    dp.register_message_handler(start_func, commands=['start'], state=None)
    dp.register_message_handler(cancel_func, commands=['cancel'], state='*')