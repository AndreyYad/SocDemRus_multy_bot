from aiogram import F

from functional_sectors.new_post_redactors.callbacks import register_callbacks_new_post_redactors

async def registration_callback():
    await register_callbacks_new_post_redactors()