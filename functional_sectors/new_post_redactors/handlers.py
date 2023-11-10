from aiogram import types
from aiogram.dispatcher import FSMContext

from main_modules.bot_cmds import reply_msg, check_user_in_chat
from main_modules.bot_dispatcher import dp
from main_modules.config import CHATS
from main_modules.state_machine import FSMClient
from main_modules.reset_state import reset
from modules.messages import MESSAGES
from modules.new_post import new_post_to_red

@dp.message_handler(commands=['new_post'], state=None)
async def cmd_new_post_func(msg: types.Message):
    print(1)
    if msg.chat.type == 'private' and await check_user_in_chat(msg.from_id, CHATS['redactors']):
        print(2)
        await FSMClient.new_post_text.set()
        await reply_msg(msg, MESSAGES['new_post_text'])

@dp.message_handler(state=FSMClient.new_post_text)
async def new_post_text_func(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['new_post_text'] = msg.text
    await FSMClient.next()
    await reply_msg(msg, MESSAGES['new_post_headline'])

@dp.message_handler(state=FSMClient.new_post_headline)
async def new_post_headline_func(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['new_post_headline'] = msg.text
    await FSMClient.next()
    await reply_msg(msg, MESSAGES['new_post_picture'])

@dp.message_handler(state=FSMClient.new_post_picture, content_types=["photo", "text"])
async def new_post_picture_func(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if msg.text in ['нет', 'не будет']:
            data['new_post_picture'] = msg.text
        elif msg.photo:
            data['new_post_picture'] = msg.photo[-1].file_id
        else:
            await reset(msg, state)
            return
        await new_post_to_red(msg.from_user, data)
    await state.finish()
    await reply_msg(msg, 'asdasd')

@dp.message_handler(regexp='^\+текст .')
async def add_text_po_post(msg: types.Message):
    print(msg)
    if msg.chat.id == CHATS['redactors']:
        print(msg)