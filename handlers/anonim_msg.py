from aiogram import types
from aiogram.dispatcher import FSMContext

from modules.bot_cmds import reply_msg
from modules.data import send_anonim_msg
from modules.messages import MESSAGES
from modules.states import FSMClient
from modules.bot_dispatcher import dp

# commands=['msg_ok']
async def cmd_send_anonim_msg_func(msg: types.Message):
    if msg.chat.type == 'private':
        await FSMClient.anonim_msg_text.set()
        await reply_msg(msg, MESSAGES['anonim_msg_info'])

# state=FSMClient.anonim_msg_text
async def get_anonim_msg_func(msg: types.Message, state: FSMContext):
    await reply_msg(msg, await send_anonim_msg(msg))
    await state.finish()

def register_handlers():
    dp.register_message_handler(cmd_send_anonim_msg_func, commands=['msg_ok'], state=None)
    dp.register_message_handler(get_anonim_msg_func, state=FSMClient.anonim_msg_text)