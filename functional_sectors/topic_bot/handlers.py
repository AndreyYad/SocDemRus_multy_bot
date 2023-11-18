# from main_modules.bot_dispatcher import *
# from aiogram.utils import executor
# from aiogram.types import Message

# from .topic_signalbot import topic_signalbot

# signalbot=topic_signalbot()

# @dp.message_handler(commands = ['init_tunnel'])
# async def init_tunnel(msg: Message):
#     await signalbot.init_tunnel(msg)
# @dp.message_handler(commands = ['bind'])
# async def connect_to_tunnel(msg:Message):
#     await signalbot.connect_to_tunnel(msg)
# @dp.message_handler()
# async def process_any_msg(msg:Message):
#     await signalbot.process_any_msg(msg)