from handlers import *
from sys import modules

def register_all_handlers():
    for module in modules.keys():
        if module.startswith('handlers.'):
            print(modules[module])
            modules[module].register_handlers()