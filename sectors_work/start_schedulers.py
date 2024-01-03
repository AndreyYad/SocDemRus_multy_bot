from asyncio import AbstractEventLoop

from functional_sectors.new_post_redactors.loop import new_post_loop
from functional_sectors.repost_from_vk.loop import repost_from_vk_loop

async def start_loop(loop: AbstractEventLoop):
    await new_post_loop(loop)
    await repost_from_vk_loop(loop)