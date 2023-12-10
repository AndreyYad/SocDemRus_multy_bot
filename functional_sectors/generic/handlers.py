from aiogram import types, F, Router
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext

from main_modules.bot_cmds import reply_msg, get_chat_name, send_msg
from main_modules.reset_state import reset
from main_modules.config import DEVELOPERS
from .messages import MESSAGES

router = Router()

# CommandStart(), StateFilter(default_state)
async def start_func(msg: types.Message):
    if msg.chat.type == 'private':
        await reply_msg(msg, MESSAGES['start'])
        
# Command('cancel'), ~StateFilter(default_state)
async def cancel_func(msg: types.Message, state: FSMContext):
    await reset(msg, state)
    
# F.text.regexp(r'\A!name -\d+\Z'), StateFilter(default_state)
async def name_chat(msg: types.Message):
    if msg.chat.id in DEVELOPERS:
        await reply_msg(msg, await get_chat_name(int(msg.text[6:])))
        
# Command('debug')
async def debug(msg: types.Message):
    # print((await get_chat_member(msg.from_user.id, msg.chat.id)).status._value_)
    # print(msg.chat.id)
    if msg.chat.id in DEVELOPERS:
        # await send_msg_photo(msg.chat.id, await get_inputfile('AgACAgIAAxkBAAIDMmVsXhMkh4resfYAAWwtq_YBSghbJQACldAxG7kIYUsiIC7pD9f8AgEAAwIAA20AAzME'), '')
        # await state.set_state(FSMClient.anonim_msg_text)
        await send_msg(msg.chat.id, 'привет, это дебаг!')
        
        
async def register_handlers_generic():
    router.message.register(start_func, CommandStart(), StateFilter(default_state))
    router.message.register(cancel_func, Command('cancel'), ~StateFilter(default_state))
    router.message.register(name_chat, F.text.regexp(r'\A!name -\d+\Z'), StateFilter(default_state))
    router.message.register(debug, Command('debug'))