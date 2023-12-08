from loguru import logger
from asyncio import run

from main_modules.dispatcher import dp
from main_modules.bot import bot
from sectors_work.registration_handlers import registration_handlers
from sectors_work.registration_callback import registration_callback
from sectors_work.create_db import start_create_database

registration_handlers()
registration_callback()

start_create_database()

logger.info('Бот запущен!')
run(dp.start_polling(bot))