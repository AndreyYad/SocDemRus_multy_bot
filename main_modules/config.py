'''
Модуль для получение информации из конфига
'''

from json import load
from loguru import logger

with open('config.json') as file:
    config = load(file)

TOKEN = config.get('token')
DEBUG = config.get('debug')
CHATS = config.get('chats')
URLS = config.get('urls')
CHANNEL = config.get('channel')
DEVELOPERS = config.get('developers')
MAIN_RED_ID = config.get('main_red_id')
COULDDAWN_ANONIM_MSG = config.get('coulddawn_anonim_msg')
TIME_FOR_REPOST = config.get('time_for_repost')
ID_EMPTY_PICTURE = config.get('id_empty_picture')

logger.info('Конфиг прочитан')