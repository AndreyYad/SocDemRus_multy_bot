from functional_sectors.new_post_redactors.callbacks import callback
from main_modules.bot_dispatcher import dp

def registration_callback():
    dp.register_callback_query_handler(callback)