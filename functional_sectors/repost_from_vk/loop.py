# from apscheduler.schedulers.asyncio import AsyncIOScheduler
from asyncio import AbstractEventLoop

async def check_posts_in_vk():
    pass
    
async def repost_from_vk_loop(loop: AbstractEventLoop):
    loop.create_task(check_posts_in_vk())