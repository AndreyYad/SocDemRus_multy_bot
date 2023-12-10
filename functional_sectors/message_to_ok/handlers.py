from aiogram import types, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.filters import Command, StateFilter

from main_modules.bot_cmds import reply_msg, send_msg
from sectors_work.state_machine import FSMClient
from main_modules.config import CHATS
from .modules.send_message_to_ok import send_anonim_msg
from .modules.database import get_author_id
from .modules.messages import MESSAGES

router = Router()

# Command('msg_ok'), StateFilter(default_state)
async def cmd_send_anonim_msg_func(msg: types.Message, state: FSMContext):
    if msg.chat.type == 'private':
        await state.set_state(FSMClient.anonim_msg_text)
        await reply_msg(msg, MESSAGES['anonim_msg_info'])

# StateFilter(FSMClient.anonim_msg_text)
async def get_anonim_msg_func(msg: types.Message, state: FSMContext):
    await reply_msg(msg, await send_anonim_msg(msg))
    await state.clear()
    
# F.text.regexp(r'\A!')
async def reaply_to_msg_in_ok(msg: types.Message):
    reaply_msg = msg.reply_to_message
    author_id = await get_author_id(reaply_msg.message_id)
    if author_id != None:
        await send_msg(author_id, MESSAGES['answer'].format(msg.text[1:]))
        await reply_msg(msg, MESSAGES['answer_sent'])
            
async def register_handlers_message_to_ok():
    router.message.register(cmd_send_anonim_msg_func, Command('msg_ok'), StateFilter(default_state))
    router.message.register(get_anonim_msg_func, F.text ,StateFilter(FSMClient.anonim_msg_text))
    router.message.register(reaply_to_msg_in_ok, F.text.regexp(r'\A!.') & (F.chat.id == CHATS['org_com']) & (F.reply_to_message != None))