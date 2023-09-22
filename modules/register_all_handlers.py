from handlers import *
from sys import modules

def register_all_handlers():
    for module in modules.keys():
        if module.startswith('handlers.'):
            modules[module].register_handlers()
            print('{} - зарегистрирован'.format(modules[module].__name__))