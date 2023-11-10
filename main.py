from aiogram.utils import executor

from main_modules.bot_dispatcher import dp
from main_modules.imports import start_modules_import

from sys import modules

start_modules_import()

print(modules.keys())

executor.start_polling(dp)