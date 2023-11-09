from aiogram import types

from ...generic.bot_cmds import check_user_in_chat, send_msg, get_chat_name
from ...generic.config import CHATS, COULDDAWN_ANONIM_MSG
from .database import set_end_cd, get_end_cd, save_sent_message
from .messages import MESSAGES

async def send_anonim_msg(msg: types.Message):
    user_id = msg.from_user.id
    msg_time = msg.date.timestamp()
    if await check_user_in_chat(user_id, CHATS['work']):
        cd = await get_end_cd(user_id) - msg_time
        if cd <= 0:
            await set_end_cd(user_id, msg_time + COULDDAWN_ANONIM_MSG)
            for chat_id in [CHATS['org_com'], CHATS['test_anon']][int(msg.text.startswith('test//')):]:
                msg_id = (await send_msg(chat_id, MESSAGES['msg_in_ok'].format(msg.text))).message_id
                if chat_id == CHATS['org_com']:
                    await save_sent_message(msg_id, user_id)
            return MESSAGES['msg_sent'].format(await get_chat_name(CHATS['org_com']))
        else:
            return MESSAGES['cd_not_pass'].format(await __get_coulddawn_text(cd))
    else:
        return MESSAGES['not_in_sdr'].format(await get_chat_name(CHATS['work']))
    
async def __get_coulddawn_text(coulddawn: int):
    '''Текст об окончании кулдауна'''
    if coulddawn > 59:
        result = '{} мин.'.format(int(coulddawn // 60))
    else:
        result = '{} сек.'.format(int(coulddawn))
    return result