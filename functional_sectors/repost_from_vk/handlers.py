from aiogram import types, Router
from aiogram.fsm.state import default_state
from aiogram.filters import Command, StateFilter
# from loguru import logger

from main_modules.bot_cmds import send_msg
from main_modules.config import CHANNEL
from .modules.parsing import get_last_post

router = Router()

async def test_msg_channel(msg: types.Message):
    await send_msg(msg.chat.id, await get_last_post())
        
async def register_handlers_repost_from_vk():
    router.message.register(test_msg_channel, Command('test'), StateFilter(default_state))