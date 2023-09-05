from json import dump

config = {
    'token' : ''
}

with open('config.json', 'w') as file:
    dump(config, file, indent=4)