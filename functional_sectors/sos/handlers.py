from aiogram import types
from aiogram.dispatcher import FSMContext

from ..generic.bot_cmds import reply_msg
from ..generic.messages import MESSAGES
from ..generic.state_machine import FSMClient
from ..generic.bot_dispatcher import dp
from ..generic.reset_state import reset
from .modules.bans_in_chats import ban_in_all_chats

@dp.message_handler(commands=['sos'], state=None)
async def cmd_sos_func(msg: types.Message):
    if msg.chat.type == 'private':
        await FSMClient.sos_confirmation.set()
        await reply_msg(msg, MESSAGES['sos_confirmation_1'])

@dp.message_handler(state=FSMClient.sos_confirmation)
async def sos_confirmation_func(msg: types.Message, state: FSMContext):
    if msg.text != 'Да, я уверен, удалите меня':
        await reset(msg, state)
    else:
        await state.finish()
        await ban_in_all_chats(msg.from_id)
        await reply_msg(msg, MESSAGES['sos_succes'])