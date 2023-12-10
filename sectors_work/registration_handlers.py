from functional_sectors.generic.handlers import register_handlers_generic
from functional_sectors.message_to_ok.handlers import register_handlers_message_to_ok
from functional_sectors.new_post_redactors.handlers import register_handlers_new_post_redactors
from functional_sectors.sos.handlers import register_handlers_sos

async def registration_handlers():
    await register_handlers_generic()
    await register_handlers_new_post_redactors()
    await register_handlers_message_to_ok()
    await register_handlers_sos()