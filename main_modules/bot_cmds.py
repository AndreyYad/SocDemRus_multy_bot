'''
Модуль с командами для бота
'''

from aiogram import types, utils

from main_modules.bot_dispatcher import dp
from .config import TOKEN, CHATS

async def send_msg(chat_id: int, text: str, markup: types.InlineKeyboardMarkup=types.InlineKeyboardMarkup(), web_prew: bool=False, **kwargs):
    '''Отправка сообщения'''
    return await dp.bot.send_message(chat_id, text, reply_markup=markup, parse_mode='html', disable_web_page_preview=not web_prew, **kwargs)

async def send_msg_photo(chat_id: int, photo: types.InputFile, text: str, markup: types.InlineKeyboardMarkup=types.InlineKeyboardMarkup(), web_prew: bool=False, **kwargs):
    '''Отправка фото'''
    return await dp.bot.send_photo(chat_id, photo, text, reply_markup=markup, parse_mode='html', **kwargs)

async def reply_msg(msg: types.Message, text: str, markup: types.InlineKeyboardMarkup=types.InlineKeyboardMarkup(), web_prew: bool=False, **kwargs):
    '''Ответ на сообщение'''
    await msg.reply(text, reply_markup=markup, parse_mode='html', disable_web_page_preview=not web_prew, **kwargs)
    
async def edit_msg_text(text: str, chat_id: int, msg_id: int, markup: types.InlineKeyboardMarkup=types.InlineKeyboardMarkup(), web_prew: bool=False, **kwargs):
    '''Редактирование сообщения'''
    try:
        await dp.bot.edit_message_text(text, chat_id, msg_id, parse_mode='html', disable_web_page_preview=not web_prew, reply_markup=markup, **kwargs)
    except utils.exceptions.MessageNotModified:
        pass
    
# async def edit_msg_media(text: str, chat_id: int, msg_id: int, markup: types.InlineKeyboardMarkup=types.InlineKeyboardMarkup(), web_prew: bool=False, **kwargs):
#     '''Редактирование сообщения'''
#     await dp.bot.edit_message_media(text, chat_id, msg_id, parse_mode='html', disable_web_page_preview=not web_prew, reply_markup=markup, **kwargs)

async def edit_msg_caption(text: str, chat_id: int, msg_id: int, markup: types.InlineKeyboardMarkup=types.InlineKeyboardMarkup(), **kwargs):
    '''Редактирование подписи(текста в сообщении с медиа)'''
    try:
        await dp.bot.edit_message_caption(chat_id, msg_id, caption=text, parse_mode='html', reply_markup=markup, **kwargs)
    except utils.exceptions.MessageNotModified:
        pass

async def get_chat_member(user_id: int, chat_id: int):
    '''Получение пользователя из чата'''
    return (await dp.bot.get_chat_member(chat_id, user_id))

async def check_user_in_chat(user_id: int, chat_id: int):
    '''Проверка на членство в чате'''
    return (await get_chat_member(user_id, chat_id))['status'] != 'left'

async def get_name_user(user_id: int):
    '''
    Получение имени пользователя
    
    Только если он состоит в Рабочем чате СДР
    '''
    return (await get_chat_member(user_id, CHATS['work']))['user']['first_name']

async def get_chat_name(chat_id: int):
    '''Получение имени чата'''
    return (await dp.bot.get_chat(chat_id))['title']

async def send_to_topic(text:str,topic_chat_id:int,topic_id:int, **kwargs):
    await dp.bot.send_message(topic_chat_id,text,parse_mode="html",reply_to_message_id=topic_id,**kwargs)

async def forward_msg(chat_id_to: int, chat_id_from: int, msg_id: int, **kwargs):
    '''Пересылка сообщения'''
    await dp.bot.forward_message(chat_id_to, chat_id_from, msg_id, **kwargs)
    
async def get_inputfile(file_id: str):
    '''Получение файла по его айди'''
    return types.InputFile.from_url(
        'https://api.telegram.org/file/bot{}/{}'.format(
            TOKEN, 
            (await dp.bot.get_file(file_id)).file_path
        )
    )

if __name__ == '__main__':
    # run()
    pass