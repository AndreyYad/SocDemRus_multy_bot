from aiogram.utils import executor
from loguru import logger
from sys import modules

from main_modules.bot_dispatcher import dp
from sectors_work.registration_handlers import register_handlers
from sectors_work.registration_callback import registration_callback
from sectors_work.create_db import start_create_database

register_handlers()
registration_callback()
start_create_database()

executor.start_polling(dp)