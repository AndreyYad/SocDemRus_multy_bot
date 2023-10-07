from generic.bot_dispatcher import *
from aiogram.utils import executor
from aiogram.types import Message

from topic_signalbot import TopicSignalbot
from ..generic.bot_cmds import *

signalbot=TopicSignalbot()

@dp.message_handler(commands = ['init_tunnel'])
async def init_tunnel(msg: Message):
    await signalbot.init_tunnel(msg)
@dp.message_handler(commands = ['bind'])
async def connect_to_tunnel(msg:Message):
    await signalbot.connect_to_tunnel(msg)
@dp.message_handler(commands=["test"], state=None)
async def test(msg:Message):
    await msg.reply("Я вроде работаю, kek...")
@dp.message_handler()
async def process_any_msg(msg:Message):
    await signalbot.process_any_msg(msg)