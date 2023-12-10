# from apscheduler.schedulers.asyncio import AsyncIOScheduler
from asyncio import sleep, AbstractEventLoop
from time import time

from .modules.database import get_post_data, get_posts_id, add_time_repost, get_msg_id_from_post_id
from .modules.new_post import get_text_msg, send_post_from_bd
from .modules.messages import MESSAGES
from main_modules.config import CHATS
from main_modules.bot_cmds import edit_msg_any

async def repost_new_post():
    while True:
        for post_id in await get_posts_id():
            if time() >= (await get_post_data(post_id))[4]:
                await add_time_repost(post_id)
                old_msg_id = await get_msg_id_from_post_id(post_id)
                new_msg_url = (await send_post_from_bd(post_id)).get_url()
                await edit_msg_any(
                    await get_text_msg(post_id, type=2, msg_url=new_msg_url),
                    CHATS['redactors'],
                    old_msg_id
                )
        await sleep(30)
    
async def new_post_loop(loop: AbstractEventLoop):
    loop.create_task(repost_new_post())