from aiogram.utils import executor
from loguru import logger
from sys import modules

from main_modules.bot_dispatcher import dp
from main_modules.imports import start_modules_import

start_modules_import()

print(modules.keys())
logger.info('Дудлиду полнейший')

executor.start_polling(dp)