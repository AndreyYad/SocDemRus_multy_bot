'''
Модуль для получение информации из конфига
'''

from json import load

with open('config.json') as file:
    config = load(file)

TOKEN = config.get('token')
DEBUG = config.get('debug')
CHATS = config.get('chats')
COULDDAWN_ANONIM_MSG = config.get('coulddawn_anonim_msg')