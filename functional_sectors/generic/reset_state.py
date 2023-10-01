from aiogram import types
from aiogram.dispatcher import FSMContext

from functional_sectors.generic.bot_cmds import reply_msg
from functional_sectors.generic.messages import MESSAGES

async def reset(msg: types.Message, state: FSMContext):
    '''Сброс состояния'''
    async with state.proxy() as data:
        if data.state != None:
            await state.finish()
            await reply_msg(msg, MESSAGES['reset'])