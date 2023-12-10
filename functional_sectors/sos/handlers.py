from aiogram import types, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.filters import Command, StateFilter

from main_modules.bot_cmds import reply_msg, check_user_in_chat
from main_modules.reset_state import reset
from main_modules.config import CHATS
from sectors_work.state_machine import FSMClient
from .modules.bans_in_chats import ban_in_all_chats
from .modules.messages import MESSAGES

router = Router()

# Command('sos'), StateFilter(default_state)
async def cmd_sos_func(msg: types.Message, state: FSMContext):
    if msg.chat.type == 'private' and await check_user_in_chat(msg.from_user.id, CHATS['work']):
        await state.set_state(FSMClient.sos_confirmation)
        await reply_msg(msg, MESSAGES['sos_confirmation'])

# StateFilter(FSMClient.sos_confirmation)
async def sos_confirmation_func(msg: types.Message, state: FSMContext):
    if msg.text != 'Да, я уверен, удалите меня':
        await reset(msg, state)
    else:
        await state.clear()
        await ban_in_all_chats(msg.from_user.id)
        await reply_msg(msg, MESSAGES['sos_succes'])
        
async def register_handlers_sos():
    router.message.register(cmd_sos_func, Command('sos'), StateFilter(default_state))
    router.message.register(sos_confirmation_func, StateFilter(FSMClient.sos_confirmation))