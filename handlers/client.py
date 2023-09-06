from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from modules.bot_cmds import *
from modules.messages import MESSAGES
from modules.bot_dispatcher import dp
from modules.data import send_anonim_msg

class FSMClient(StatesGroup):
    anonim_msg_text = State()

# commands=['start']
async def start_func(msg: types.Message):
    if msg.chat.type == 'private':
        await msg.reply(MESSAGES['start'])

# commands=['cancel']
async def cancel_func(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if data.state != None:
            await state.finish()
            await msg.reply(MESSAGES['reset'])

# commands=['msg_ok']
async def cmd_send_anonim_msg_func(msg: types.Message):
    if msg.chat.type == 'private':
        await FSMClient.anonim_msg_text.set()
        await msg.reply(MESSAGES['anonim_msg_info'])

# state=FSMClient.anonim_msg_text
async def get_anonim_msg_func(msg: types.Message, state: FSMContext):
    await msg.reply(await send_anonim_msg(msg))
    await state.finish()

def register_handlers_client():
    dp.register_message_handler(start_func, commands=['start'], state=None)
    dp.register_message_handler(cancel_func, commands=['cancel'], state='*')
    dp.register_message_handler(cmd_send_anonim_msg_func, commands=['msg_ok'], state=None)
    dp.register_message_handler(get_anonim_msg_func, state=FSMClient.anonim_msg_text)