from os import scandir
from importlib import import_module

def _import(
          pack: str, 
          module: str, 
          object_: str | None=None,
          call: list[any] | None=None
            ):
    try:
        if object_ != None:
            if call != None:
                return import_module(f'functional_sectors.{pack}.{module}').__dict__[object_](*call)
            else:
                return import_module(f'functional_sectors.{pack}.{module}').__dict__[object_]
        else:
            return import_module(f'functional_sectors.{pack}.{module}')
    except ModuleNotFoundError:
        pass
    except TypeError:
        pass

def get_states():
    state_classes = []

    for it in scandir('functional_sectors/'):
        if it.is_dir() and it.name != '__pycache__':
            if _import(it.name, 'states', 'States') != None:
                state_classes.append(_import(it.name, 'states', 'States'))

    return state_classes

def start_modules_import():
    for it in scandir('functional_sectors/'):
        if it.is_dir() and it.name != '__pycache__':
            _import(it.name, 'handlers')
            _import(it.name, 'database', 'create_database', call=[])