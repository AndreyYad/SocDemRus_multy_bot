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
DEVELOPERS = config.get('developers')
COULDDAWN_ANONIM_MSG = config.get('coulddawn_anonim_msg')

logger.info('Конфиг прочитан')