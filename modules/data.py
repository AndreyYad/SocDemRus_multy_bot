from aiogram import types

from modules.sql_cmds import set_end_cd, get_end_cd
from modules.bot_cmds import *
from modules.config import CHATS, COULDDAWN_ANONIM_MSG

async def send_anonim_msg(msg: types.Message):
    user_id = msg.from_user.id
    msg_time = msg.date.timestamp()
    if await check_user_in_chat(user_id, CHATS['work']):
        cd = await get_end_cd(user_id) - msg_time
        if cd <= 0:
            await set_end_cd(user_id, msg_time + COULDDAWN_ANONIM_MSG)
            for chat_id in [CHATS['org_com'], CHATS['test_anon']][int(msg.text.startswith('test//')):]:
                await send_msg(chat_id, msg.text)
            return 'Сообщение отправлено в "{}"!'.format(await get_chat_name(CHATS['org_com']))
        else:
            return 'Ещё один запрос сможете отправить только через {}'.format(await get_coulddawn_text_(cd))
    else:
        return 'Вы не состоите в "{}"!'.format(await get_chat_name(CHATS['work']))
    
async def get_coulddawn_text_(coulddawn: int):
    '''Текст об окончании кулдауна'''
    if coulddawn > 59:
        result = '{} мин.'.format(int(coulddawn // 60))
    else:
        result = '{} сек.'.format(int(coulddawn))
    return result