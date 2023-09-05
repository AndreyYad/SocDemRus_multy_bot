from aiogram.utils import executor

from modules.bot_dispatcher import dp
from handlers import client

client.register_handlers_client()

executor.start_polling(dp)