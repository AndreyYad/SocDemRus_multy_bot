'''
Модуль с командами для бота
'''

from loguru import logger
from aiogram import types
from aiogram import exceptions
from aiogram.types.input_media_photo import InputMediaPhoto


from .config import TOKEN, CHATS
from main_modules.bot import bot

empty_markups = types.InlineKeyboardMarkup(inline_keyboard=[[]])

async def send_msg(chat_id: int, text: str, markup: types.InlineKeyboardMarkup=empty_markups, **kwargs):
    '''Отправка сообщения'''
    return await bot.send_message(chat_id, text, reply_markup=markup, **kwargs)

async def send_msg_photo(chat_id: int, photo: types.InputFile, text: str, markup: types.InlineKeyboardMarkup=empty_markups, **kwargs):
    '''Отправка фото'''
    return await bot.send_photo(chat_id, photo, caption=text, reply_markup=markup, **kwargs)

async def reply_msg(msg: types.Message, text: str, markup: types.InlineKeyboardMarkup=empty_markups, **kwargs):
    '''Ответ на сообщение'''
    await msg.reply(text, reply_markup=markup, **kwargs)
    
async def edit_msg_text(text: str, chat_id: int, msg_id: int, markup: types.InlineKeyboardMarkup=empty_markups, **kwargs):
    '''Редактирование сообщения'''
    try:
        await bot.edit_message_text(text, chat_id, msg_id, reply_markup=markup, **kwargs)
        return True
    except exceptions.TelegramBadRequest as error:
        logger.error(error)
        return False

async def edit_msg_caption(text: str, chat_id: int, msg_id: int, markup: types.InlineKeyboardMarkup=empty_markups, **kwargs):
    '''Редактирование подписи(текста в сообщении с медиа)'''
    try:
        await bot.edit_message_caption(chat_id, msg_id, caption=text, reply_markup=markup, **kwargs)
        return True
    except exceptions.TelegramBadRequest as error:
        logger.error(error)
        return False
    
async def edit_msg_media(chat_id: int, msg_id: int, markup: types.InlineKeyboardMarkup=empty_markups, file: InputMediaPhoto | None=None, file_id: str=''):
    if file is None:
        file = await get_inputfile(file_id)
    await bot.edit_message_media(InputMediaPhoto(media=file), chat_id, msg_id, reply_markup=markup)
    
async def edit_msg_any(text: str, chat_id: int, msg_id: int, markup: types.InlineKeyboardMarkup=empty_markups, **kwargs):
    '''Редактирвоание любого сообщения с текстом'''
    args = [text, chat_id, msg_id, markup]
    if not await edit_msg_caption(*args, **kwargs):
        await edit_msg_text(*args, **kwargs)
        
async def delete_msg(chat_id: int, msg_id: int):
    '''Удаление сообщения'''
    await bot.delete_message(chat_id, msg_id)

async def get_chat_member(user_id: int, chat_id: int):
    '''Получение пользователя из чата'''
    return (await bot.get_chat_member(chat_id, user_id))

async def check_user_in_chat(user_id: int, chat_id: int):
    '''Проверка на членство в чате'''
    return (await get_chat_member(user_id, chat_id)).status != 'left'

async def get_name_user(user_id: int):
    '''
    Получение имени пользователя
    
    Только если он состоит в Рабочем чате СДР
    '''
    return (await get_chat_member(user_id, CHATS['work'])).user.first_name

async def get_chat_name(chat_id: int):
    '''Получение имени чата'''
    return (await bot.get_chat(chat_id)).title

# async def send_to_topic(text:str,topic_chat_id:int,topic_id:int, **kwargs):
#     await bot.send_message(topic_chat_id,text,parse_mode="html",reply_to_message_id=topic_id,**kwargs)

async def forward_msg(chat_id_to: int, chat_id_from: int, msg_id: int, **kwargs):
    '''Пересылка сообщения'''
    await bot.forward_message(chat_id_to, chat_id_from, msg_id, **kwargs)
    
async def get_inputfile(file_id: str):
    '''Получение файла по его айди'''
    return types.input_file.URLInputFile(
        'https://api.telegram.org/file/bot{}/{}'.format(
            TOKEN, 
            (await bot.get_file(file_id)).file_path
        )
    )

if __name__ == '__main__':
    # run()
    pass