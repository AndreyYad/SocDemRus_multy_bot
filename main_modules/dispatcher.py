from aiogram.dispatcher.dispatcher import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from functional_sectors.generic import handlers as generic_handlers
from functional_sectors.sos import handlers as sos_handlers
from functional_sectors.message_to_ok import handlers as message_to_ok_handlers
from functional_sectors.new_post_redactors import handlers as new_post_redactors_handlers
from functional_sectors.new_post_redactors import callbacks as new_post_redactors_callbacks

storage = MemoryStorage()

dp = Dispatcher(storage=storage)

dp.include_routers(
    generic_handlers.router,
    sos_handlers.router,
    message_to_ok_handlers.router,
    new_post_redactors_handlers.router,
    new_post_redactors_callbacks.router
)