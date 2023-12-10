from loguru import logger
from asyncio import run, get_event_loop

from main_modules.dispatcher import dp
from main_modules.bot import bot
from sectors_work.registration_handlers import registration_handlers
from sectors_work.registration_callback import registration_callback
from sectors_work.create_db import start_create_database
from sectors_work.start_schedulers import start_loop

async def main():
    await registration_handlers()
    await registration_callback()
    
    loop = get_event_loop()
    await start_loop(loop)
    logger.info('Бот запущен!')
    await loop.create_task(dp.start_polling(bot))

if __name__ == '__main__':
    start_create_database()
    try:
        run(main())
    except KeyboardInterrupt:
        pass