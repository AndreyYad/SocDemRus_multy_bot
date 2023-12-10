from aiogram import types, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.filters import Command, StateFilter
# from loguru import logger

from main_modules.bot_cmds import reply_msg, check_user_in_chat, edit_msg_any, edit_msg_media, get_chat_member
from main_modules.config import CHATS
from main_modules.reset_state import reset
from sectors_work.state_machine import FSMClient
from .modules.messages import MESSAGES
from .modules.new_post import send_post_from_bd, get_text_msg, send_to_design
from .modules.database import save_new_post, get_post_id_from_msg_id, change_post_data, get_author, delete_post_in_bd
from .modules.markups import markup_like

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

# (F.reply_to_message != None) & ((F.text.regexp(r'\A!(текст|заголовок) .')) | (F.caption == '!фото') & (F.content_type == 'photo'))
async def change_post_data_message(msg: types.Message):
    msg_text = msg.text
    if msg_text is None:
        msg_text = msg.caption
    repling = msg.reply_to_message
    post_id = await get_post_id_from_msg_id(repling.message_id)
    if msg.chat.id == CHATS['redactors'] and post_id is not None:
        if msg_text.startswith('!т'):
            await change_post_data(post_id, type_data='text', new_data=msg_text.replace('!текст ', ''))
            await reply_msg(msg, MESSAGES['change_succes'].format('Текст'))
        elif msg_text.startswith('!з'):
            await change_post_data(post_id, type_data='headline', new_data=msg_text.replace('!заголовок ', ''))
            await reply_msg(msg, MESSAGES['change_succes'].format('Заголовок'))
        else:
            await change_post_data(post_id, type_data='picture', new_data=msg.photo[-1].file_id)
            if repling.content_type == 'photo':
                await edit_msg_media(msg.chat.id, repling.message_id, file_id=msg.photo[-1].file_id)
            await reply_msg(msg, MESSAGES['change_photo_succes'])
        
        await edit_msg_any(
            text=await get_text_msg(post_id),
            chat_id=msg.chat.id,
            msg_id=repling.message_id,
            markup=await markup_like()
        )
        
        await send_to_design(post_id)
        
async def delete_post(msg: types.Message):
    user_id = msg.from_user.id
    repling = msg.reply_to_message
    post_id = await get_post_id_from_msg_id(repling.message_id)
    if post_id is not None:
        if (await get_chat_member(user_id, CHATS['redactors'])).status._value_ in ['creator', 'administrator'] or user_id == await get_author(post_id=post_id):
            await edit_msg_any(
                await get_text_msg(post_id, type=3), 
                CHATS['redactors'], 
                repling.message_id
            )
            await delete_post_in_bd(post_id)
        else:
            await reply_msg(msg, MESSAGES['delete_access'])
        
async def register_handlers_new_post_redactors():
    router.message.register(cmd_new_post_func, Command('new_post'), StateFilter(default_state))
    router.message.register(new_post_text_func, F.text, StateFilter(FSMClient.new_post_text))
    router.message.register(new_post_headline_func, F.text, StateFilter(FSMClient.new_post_headline))
    router.message.register(new_post_picture_func, F.text | F.photo, StateFilter(FSMClient.new_post_picture))
    router.message.register(change_post_data_message, (F.reply_to_message != None) & ((F.text.regexp(r'\A!(текст|заголовок) .')) | (F.caption == '!фото') & (F.content_type == 'photo') & (F.reply_to_message.content_type == 'photo')))
    router.message.register(delete_post, (F.reply_to_message != None) & (F.text == '!удалить') & (F.chat.id == CHATS['redactors']))