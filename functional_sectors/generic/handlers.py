from aiogram import types
from aiogram.dispatcher import FSMContext

from main_modules.bot_cmds import reply_msg, get_chat_name, send_msg_photo, get_inputfile
from main_modules.reset_state import reset
from main_modules.config import DEVELOPERS
from main_modules.bot_dispatcher import dp
from .messages import MESSAGES

# commands=['start'], state=None
async def start_func(msg: types.Message):
    if msg.chat.type == 'private':
        await reply_msg(msg, MESSAGES['start'])
        

# commands=['cancel'], state='*'
async def cancel_func(msg: types.Message, state: FSMContext):
    await reset(msg, state)
    
# regexp='\A!name -\d+\Z', state=None
async def name_chat(msg: types.Message):
    if msg.chat.id in DEVELOPERS:
        await reply_msg(msg, await get_chat_name(int(msg.text[6:])))
        
# commands=['debug']
async def debug(msg: types.Message):
    if msg.chat.id in DEVELOPERS:
        await send_msg_photo(msg.chat.id, await get_inputfile('AgACAgIAAxkBAAIDMmVsXhMkh4resfYAAWwtq_YBSghbJQACldAxG7kIYUsiIC7pD9f8AgEAAwIAA20AAzME'), '')
        
def register_handlers_generic():
    dp.register_message_handler(start_func, commands=['start'], state=None)
    dp.register_message_handler(cancel_func, commands=['cancel'], state='*')
    dp.register_message_handler(name_chat, regexp='\A!name -\d+\Z', state=None)
    dp.register_message_handler(debug, commands=['debug'])