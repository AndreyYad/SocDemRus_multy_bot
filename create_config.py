from json import dump

config = {
    "token" : "",
    "debug" : False, 
    "chats" : {
        "work" : 0,
        "org_com" : 0,
        "test_anon" : 0,
        "redactors" : 0,
        "designers" : 0
    },
    "coulddawn_anonim_msg" : 3600
}

with open('config.json', 'w') as file:
    dump(config, file, indent=4)