from aiogram import types
from aiogram.dispatcher import FSMContext

from modules.bot_cmds import *
from modules.data import *
from modules.messages import MESSAGES
from modules.states import FSMClient
from modules.bot_dispatcher import dp
from modules.generator_expressions import generator_expression

from handlers.client import _reset

# commands=['sos']
async def cmd_sos_func(msg: types.Message):
    if msg.chat.type == 'private':
        await FSMClient.sos_confirmation_1.set()
        await reply_msg(msg, MESSAGES['sos_confirmation_1'])

# state=FSMClient.sos_confirmation_1
async def sos_confirmation_1_func(msg: types.Message, state: FSMContext):
    if msg.text != 'Да, я уверен, удалите меня':
        await _reset(msg, state)
    else:
        await FSMClient.next()
        expression = await generator_expression()
        async with state.proxy() as data:
            data['sos_confirmation_2'] = expression['result']
        await reply_msg(msg, MESSAGES['sos_confirmation_2'].format(expression['expression']))

# state=FSMClient.sos_confirmation_2
async def sos_confirmation_2_func(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if msg.text != data['sos_confirmation_2']:
            await _reset(msg, state)
        else:
            await state.finish()
            await ban_in_all_chats(msg.from_id)
            await reply_msg(msg, MESSAGES['sos_succes'])

def register_handlers():
    dp.register_message_handler(cmd_sos_func, commands=['msg_ok'], state=None)
    dp.register_message_handler(sos_confirmation_1_func, state=FSMClient.sos_confirmation_1)
    dp.register_message_handler(sos_confirmation_2_func, state=FSMClient.sos_confirmation_2)