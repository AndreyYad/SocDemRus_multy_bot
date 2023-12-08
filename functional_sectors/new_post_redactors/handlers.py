from aiogram import types, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.filters import Command, StateFilter

from main_modules.bot_cmds import reply_msg, check_user_in_chat
from main_modules.config import CHATS
from sectors_work.state_machine import FSMClient
from main_modules.reset_state import reset
from .modules.messages import MESSAGES
from .modules.new_post import send_post_from_bd
from .modules.database import save_new_post

router = Router()

# commands=['new_post'], state=None
async def cmd_new_post_func(msg: types.Message, state: FSMContext):
    if msg.chat.type == 'private' and await check_user_in_chat(msg.from_user.id, CHATS['redactors']):
        await state.set_state(FSMClient.new_post_text)
        await reply_msg(msg, MESSAGES['new_post_text'])

# state=FSMClient.new_post_text
async def new_post_text_func(msg: types.Message, state: FSMContext):
    await state.update_data(new_post_text=msg.text)
    await state.set_state(FSMClient.new_post_headline)
    await reply_msg(msg, MESSAGES['new_post_headline'])

# state=FSMClient.new_post_headline
async def new_post_headline_func(msg: types.Message, state: FSMContext):
    await state.update_data(new_post_headline=msg.text)
    await state.set_state(FSMClient.new_post_picture)
    await reply_msg(msg, MESSAGES['new_post_picture'])

# state=FSMClient.new_post_picture, content_types=["photo", "text"]
async def new_post_picture_func(msg: types.Message, state: FSMContext):
    if msg.text in ['нет', 'не будет']:
        await state.update_data(new_post_picture=msg.text)
    elif msg.photo:
        await state.update_data(new_post_picture=msg.photo[-1].file_id)
    else:
        await reset(msg, state)
        return
    post_id = await save_new_post(msg.from_user.id, await state.get_data())
    await send_post_from_bd(post_id)
        # await new_post_to_red(msg.from_user, data)
    await state.clear()
    await reply_msg(msg, 'Предложение поста отправленно в беседу редакторов!')

# regexp='\A!текст '
async def add_text_to_post(msg: types.Message):
    if msg.chat.id == CHATS['redactors']:
        print(msg)
        
def register_handlers_new_post_redactors():
    router.message.register(cmd_new_post_func, Command('new_post'), StateFilter(default_state))
    router.message.register(new_post_text_func, StateFilter(FSMClient.new_post_text))
    router.message.register(new_post_headline_func, StateFilter(FSMClient.new_post_headline))
    router.message.register(new_post_picture_func, F.text | F.photo, StateFilter(FSMClient.new_post_picture))
    router.message.register(add_text_to_post, F.text.regexp(r'\A!текст '))