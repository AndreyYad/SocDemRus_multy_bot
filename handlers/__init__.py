from os import listdir
__all__ = [file.replace('.py', '') for file in listdir('handlers') if ['__pycache__', '__init__.py'].count(file) == 0]