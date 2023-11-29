from aiogram import types
from aiogram.dispatcher import FSMContext

from main_modules.bot_cmds import reply_msg, send_msg
from sectors_work.state_machine import FSMClient
from main_modules.bot_dispatcher import dp
from main_modules.config import CHATS
from .modules.send_message_to_ok import send_anonim_msg
from .modules.database import get_author_id
from .modules.messages import MESSAGES

# commands=['msg_ok'], state=None
async def cmd_send_anonim_msg_func(msg: types.Message):
    if msg.chat.type == 'private':
        await FSMClient.anonim_msg_text.set()
        await reply_msg(msg, MESSAGES['anonim_msg_info'])

# state=FSMClient.anonim_msg_text
async def get_anonim_msg_func(msg: types.Message, state: FSMContext):
    await reply_msg(msg, await send_anonim_msg(msg))
    await state.finish()
    
# regexp='\A!'
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
            
def register_handlers_message_to_ok():
    dp.register_message_handler(cmd_send_anonim_msg_func, commands=['msg_ok'], state=None)
    dp.register_message_handler(get_anonim_msg_func, state=FSMClient.anonim_msg_text)
    dp.register_message_handler(reaply_to_msg_in_ok, regexp='\A!')