from asyncio import AbstractEventLoop

from functional_sectors.new_post_redactors.loop import new_post_loop

async def start_loop(loop: AbstractEventLoop):
    await new_post_loop(loop)