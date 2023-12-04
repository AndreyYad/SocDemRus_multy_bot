from aiogram import types
from aiogram.dispatcher import FSMContext

from main_modules.bot_cmds import reply_msg, check_user_in_chat
from main_modules.bot_dispatcher import dp
from main_modules.reset_state import reset
from main_modules.config import CHATS
from sectors_work.state_machine import FSMClient
from .modules.bans_in_chats import ban_in_all_chats
from .modules.messages import MESSAGES

# commands=['sos'], state=None
async def cmd_sos_func(msg: types.Message):
    if msg.chat.type == 'private' and await check_user_in_chat(msg.from_id, CHATS['work']):
        await FSMClient.sos_confirmation.set()
        await reply_msg(msg, MESSAGES['sos_confirmation'])

# state=FSMClient.sos_confirmation
async def sos_confirmation_func(msg: types.Message, state: FSMContext):
    if msg.text != 'Да, я уверен, удалите меня':
        await reset(msg, state)
    else:
        await state.finish()
        await ban_in_all_chats(msg.from_id)
        await reply_msg(msg, MESSAGES['sos_succes'])
        
def register_handlers_sos():
    dp.register_message_handler(cmd_sos_func, commands=['sos'], state=None)
    dp.register_message_handler(sos_confirmation_func, state=FSMClient.sos_confirmation)