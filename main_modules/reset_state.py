from aiogram import types
from aiogram.fsm.context import FSMContext

from main_modules.bot_cmds import reply_msg
from functional_sectors.generic.messages import MESSAGES

async def reset(msg: types.Message, state: FSMContext):
    '''Сброс состояния'''
    await state.clear()
    await reply_msg(msg, MESSAGES['reset'])