from aiogram.utils import executor
from asyncio import new_event_loop

from modules.bot_dispatcher import dp
from modules.sql_cmds import born_of_db
from handlers import client, debug

client.register_handlers_client()
debug.register_handlers_debug()

loop = new_event_loop()
loop.run_until_complete(born_of_db())

executor.start_polling(dp, loop=loop)