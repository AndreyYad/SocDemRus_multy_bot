from asyncio import AbstractEventLoop, sleep

from .modules.parsing import get_id_last_post, get_last_post
from .modules.json_data import save_post_id, get_saved_id_last_post, get_already_sent, set_send_status
from .modules.messages import MESSAGES
from .modules.markups import markup_new_vk_post
from .modules.send_post import send_post
from main_modules.bot_cmds import reply_msg, send_msg
from main_modules.config import MAIN_RED_ID

async def check_posts_in_vk():
    saved_id_last_post = await get_saved_id_last_post()
    id_last_post = await get_id_last_post()
    if saved_id_last_post is not None and id_last_post > saved_id_last_post:
        msg = await send_msg(MAIN_RED_ID, await get_last_post(), disable_web_page_preview=False)
        msg = await reply_msg(msg, MESSAGES['new_post_vk'], markup=await markup_new_vk_post())
        await sleep(30)
        if not await get_already_sent():
            await send_post(msg)
        else:
            await set_send_status(False)
    await save_post_id(id_last_post)
    await sleep(300)
    
async def repost_from_vk_loop(loop: AbstractEventLoop):
    loop.create_task(check_posts_in_vk())