from aiogram import types
from aiogram.dispatcher import FSMContext

from ..generic.bot_cmds import reply_msg
from ..generic.messages import MESSAGES
from ..generic.state_machine import FSMClient
from ..generic.bot_dispatcher import dp
from .modules.send_message_to_ok import send_anonym_msg

@dp.message_handler(commands=['msg_ok'], state=None)
async def cmd_send_anonim_msg_func(msg: types.Message):
    if msg.chat.type == 'private':
        await FSMClient.anonim_msg_text.set()
        await reply_msg(msg, MESSAGES['anonim_msg_info'])

@dp.message_handler(state=FSMClient.anonim_msg_text)
async def get_anonim_msg_func(msg: types.Message, state: FSMContext):
    await reply_msg(msg, await send_anonym_msg(msg))
    await state.finish()