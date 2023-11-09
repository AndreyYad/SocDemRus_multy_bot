from aiogram import types
from aiogram.dispatcher import FSMContext

from ..generic.bot_cmds import reply_msg, send_msg
from ..generic.state_machine import FSMClient
from ..generic.bot_dispatcher import dp
from ..generic.config import CHATS
from .modules.send_message_to_ok import send_anonim_msg
from .modules.database import get_author_id
from .modules.messages import MESSAGES

@dp.message_handler(commands=['msg_ok'], state=None)
async def cmd_send_anonim_msg_func(msg: types.Message):
    if msg.chat.type == 'private':
        await FSMClient.anonim_msg_text.set()
        await reply_msg(msg, MESSAGES['anonim_msg_info'])

@dp.message_handler(state=FSMClient.anonim_msg_text)
async def get_anonim_msg_func(msg: types.Message, state: FSMContext):
    await reply_msg(msg, await send_anonim_msg(msg))
    await state.finish()
    
@dp.message_handler(regexp='\A!')
async def reaply_to_msg_in_ok(msg: types.Message):
    if msg.text == '!':
        return
    reaply_msg = msg.reply_to_message
    if msg.chat.id == CHATS['org_com'] and reaply_msg != None:
        author_id = await get_author_id(reaply_msg.message_id)
        print(author_id)
        if author_id != None:
            await send_msg(author_id, MESSAGES['answer'].format(msg.text[1:]))
            await reply_msg(msg, MESSAGES['answer_sent'])