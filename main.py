from aiogram.utils import executor

from functional_sectors.generic.bot_dispatcher import dp
from functional_sectors.generic.imports import start_modules_import

from sys import modules

start_modules_import()

print(modules.keys())

executor.start_polling(dp)