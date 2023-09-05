'''
Модуль с командами для бота
'''

# from asyncio import run

from modules.bot_dispatcher import dp

async def send_msg(chat_id: int, text: str, web_prew: bool=False, **kwargs):
    '''Отправка сообщения'''
    await dp.bot.send_message(chat_id, text, parse_mode='html', disable_web_page_preview=not web_prew, **kwargs)

if __name__ == '__main__':
    # run()
    pass