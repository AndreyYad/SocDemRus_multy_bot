from os import scandir
from importlib import import_module
from loguru import logger

def _import(
          pack: str, 
          module: str, 
          object_: str | None=None,
          call: list[any] | None=None
            ):
    try:
        if object_ != None:
            if call != None:
                logger.debug(f'Попытка вызвать объект "{object_}" из "functional_sectors.{pack}.{module}" с аргументами: {call}')
                import_module(f'functional_sectors.{pack}.{module}').__dict__[object_](*call)
            else:
                logger.debug(f'Попытка вернуть объект "{object_}" из "functional_sectors.{pack}.{module}"')
                result = import_module(f'functional_sectors.{pack}.{module}').__dict__[object_]
                logger.debug('Успешно!')
                return result
        else:
            logger.debug(f'Попытка импортировать "functional_sectors.{pack}.{module}"')
            import_module(f'functional_sectors.{pack}.{module}')
            
    except ModuleNotFoundError:
        logger.warning('Не успешно! (ModuleNotFoundError)')
    except TypeError:
        logger.warning('Не успешно! (TypeError)')
    except KeyError:
        logger.warning('Не успешно! (KeyError)')
    else:
        logger.debug('Успешно!')
        return True
    return False

def get_states():
    state_classes = []

    for it in scandir('functional_sectors/'):
        if it.is_dir() and it.name != '__pycache__':
            import_states = _import(it.name, 'states', 'States')
            if import_states != None:
                state_classes.append(import_states)

    return state_classes

def start_modules_import():
    logger.info('Начало импорта хендлеров и создания баз данных секторов')
    for it in scandir('functional_sectors/'):
        if it.is_dir() and it.name != '__pycache__':
            _import(it.name, 'handlers')
            _import(it.name, 'create_database', 'create_database', call=[])