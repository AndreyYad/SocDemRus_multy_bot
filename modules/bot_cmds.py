'''
Модуль с командами для бота
'''

# from asyncio import run

from modules.bot_dispatcher import dp

async def send_msg(chat_id: int, text: str, web_prew: bool=False, **kwargs):
    '''Отправка сообщения'''
    await dp.bot.send_message(chat_id, text, parse_mode='html', disable_web_page_preview=not web_prew, **kwargs)

async def check_user_in_chat(user_id: int, chat_id: int):
    '''Проверка на членство в чате'''
    return (await dp.bot.get_chat_member(chat_id, user_id))['status'] != 'left'

async def get_chat_name(chat_id: int):
    '''Проверка на членство в чате'''
    return (await dp.bot.get_chat(chat_id))['title']

if __name__ == '__main__':
    # run()
    pass