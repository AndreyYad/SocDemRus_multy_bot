from aiogram import types
from aiogram.dispatcher import FSMContext

from modules.bot_cmds import *
from modules.messages import MESSAGES
from modules.bot_dispatcher import dp
from modules.data import *
from modules.generator_expressions import generator_expression
from modules.states import FSMClient

async def _reset(msg: types.Message, state: FSMContext):
    '''Сброс состояния'''
    async with state.proxy() as data:
        if data.state != None:
            await state.finish()
            await reply_msg(msg, MESSAGES['reset'])

# commands=['start']
async def start_func(msg: types.Message):
    if msg.chat.type == 'private':
        await reply_msg(msg, MESSAGES['start'])
        print(msg.from_user.first_name)

# commands=['cancel']
# Сброс состояния
async def cancel_func(msg: types.Message, state: FSMContext):
    await _reset(msg, state)

# --------------------------------
# -- Удаление со всех чатов СДР --
# --------------------------------

# commands=['sos']
async def cmd_sos_func(msg: types.Message):
    if msg.chat.type == 'private':
        await FSMClient.sos_confirmation_1.set()
        await reply_msg(msg, MESSAGES['sos_confirmation_1'])

# state=FSMClient.sos_confirmation_1
async def sos_confirmation_1_func(msg: types.Message, state: FSMContext):
    if msg.text != 'Да, я уверен, удалите меня':
        await _reset(msg, state)
    else:
        await FSMClient.next()
        expression = await generator_expression()
        async with state.proxy() as data:
            data['sos_confirmation_2'] = expression['result']
        await reply_msg(msg, MESSAGES['sos_confirmation_2'].format(expression['expression']))

# state=FSMClient.sos_confirmation_2
async def sos_confirmation_2_func(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if msg.text != data['sos_confirmation_2']:
            await _reset(msg, state)
        else:
            await state.finish()
            await ban_in_all_chats(msg.from_id)
            await reply_msg(msg, MESSAGES['sos_succes'])

# commands=['new_post']
async def cmd_new_post_func(msg: types.Message):
    if msg.chat.type == 'private' and await check_user_in_chat(msg.from_id, CHATS['redactors']):
        await FSMClient.new_post_text.set()
        await reply_msg(msg, MESSAGES['new_post_text'])

# state=FSMClient.new_post_text
async def new_post_text_func(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['new_post_text'] = msg.text
    await FSMClient.next()
    await reply_msg(msg, MESSAGES['new_post_headline'])

# state=FSMClient.new_post_headline
async def new_post_headline_func(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['new_post_headline'] = msg.text
    await FSMClient.next()
    await reply_msg(msg, MESSAGES['new_post_picture'])

# state=FSMClient.new_post_picture, content_types=["photo", "text"]
async def new_post_picture_func(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if msg.text in ['нет', 'не будет']:
            data['new_post_picture'] = msg.text
        elif msg.photo:
            data['new_post_picture'] = msg.photo[-1].file_id
        else:
            await _reset(msg, state)
            return
        await new_post_to_red(msg.from_user, data)
    await state.finish()
    await reply_msg(msg, 'asdasd')

# rexexp='^+текст .'
async def add_text_po_post(msg: types.Message):
    print(msg)
    if msg.chat.id == CHATS['redactors']:
        print(msg)

async def aaa(msg: types.Message):
    print(msg)

def register_handlers():
    dp.register_message_handler(start_func, commands=['start'], state=None)
    dp.register_message_handler(cancel_func, commands=['cancel'], state='*')
    dp.register_message_handler(cmd_sos_func, commands=['sos'], state=None)
    dp.register_message_handler(sos_confirmation_1_func, state=FSMClient.sos_confirmation_1)
    dp.register_message_handler(sos_confirmation_2_func, state=FSMClient.sos_confirmation_2)
    dp.register_message_handler(cmd_new_post_func, commands=['new_post'])
    dp.register_message_handler(new_post_text_func, state=FSMClient.new_post_text)
    dp.register_message_handler(new_post_headline_func, state=FSMClient.new_post_headline)
    dp.register_message_handler(new_post_picture_func, state=FSMClient.new_post_picture, content_types=["photo", "text"])
    dp.register_message_handler(add_text_po_post, regexp='^\+текст .')