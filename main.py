from aiogram.utils import executor
from loguru import logger
from sys import modules

from main_modules.bot_dispatcher import dp
from sectors_work.registration_handlers import register_handlers

register_handlers()

executor.start_polling(dp)