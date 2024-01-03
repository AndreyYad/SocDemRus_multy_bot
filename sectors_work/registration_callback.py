from aiogram import F

from functional_sectors.new_post_redactors.callbacks import register_callbacks_new_post_redactors
from functional_sectors.repost_from_vk.callbacks import register_callbacks_repost_from_vk

async def registration_callback():
    await register_callbacks_new_post_redactors()
    await register_callbacks_repost_from_vk()