from aiogram.exceptions import TelegramBadRequest

from main_modules.bot_cmds import check_user_in_chat, send_msg, get_chat_name
from main_modules.bot import bot
from main_modules.config import CHATS
from .messages import MESSAGES
    
async def ban_in_all_chats(user_id: int):
    for chat_id in CHATS.values():
        if await check_user_in_chat(user_id, chat_id):
            try:
                await bot.ban_chat_member(chat_id, user_id)
                await bot.unban_chat_member(chat_id, user_id)
            except TelegramBadRequest:
                await send_msg(user_id, MESSAGES['cant_ban_owner'].format(await get_chat_name(chat_id)))