from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from .bot_cmds import reply_msg
from .messages import MESSAGES
from .bot_dispatcher import dp
from .reset_state import reset
from .state_machine import FSMClient
from ..topic_bot.topic_signalbot import topic_signalbot

@dp.message_handler(commands=['start'], state=None)
async def start_func(msg: types.Message):
    if msg.chat.type == 'private':
        await reply_msg(msg, MESSAGES['start'])

@dp.message_handler(commands=['cancel'], state='*')
async def cancel_func(msg: types.Message, state: FSMContext):
    await reset(msg, state)

signalbot=topic_signalbot()

@dp.message_handler(commands = ['init_tunnel'])
async def init_tunnel(msg: Message):
    await signalbot.init_tunnel(msg)
@dp.message_handler(commands = ['bind'])
async def connect_to_tunnel(msg:Message):
    await signalbot.connect_to_tunnel(msg)
@dp.message_handler()
async def process_any_msg(msg:Message):
    await signalbot.process_any_msg(msg)