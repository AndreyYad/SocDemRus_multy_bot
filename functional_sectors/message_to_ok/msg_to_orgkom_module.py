from aiogram.types import Message
from ..generic.messages import MESSAGES
from ..generic.state_machine import FSMClient
from aiogram.dispatcher import FSMContext
from modules.send_message_to_ok import send_anonym_msg
from ..generic.bot_cmds import reply_msg

class MTKModule:
    async def send_anonym_msg(self,msg:Message):
        if msg.chat.type == 'private':
            await FSMClient.anonim_msg_text.set()
            await reply_msg(msg,MESSAGES['anonim_msg_info'])
    async def get_anonim_msg(self,msg: Message, state: FSMContext):
        await reply_msg(msg, await send_anonym_msg(msg))
        await state.finish()