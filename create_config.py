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
    "urls" : {
        "sdr_vk" : ""
    },
    "channel" : 0,
    "developers" : [],
    "main_red_id" : 0,
    "coulddawn_anonim_msg" : 3600,
    "time_for_repost" : 86400,
    "id_empty_picture" : "AgACAgIAAxkBAAIGnmV0opeek2Bqvjnz95kY456N0engAAIl1DEb5VypSxcXAAFfabTvYgEAAwIAA3gAAzME"
}

with open('config.json', 'w') as file:
    dump(config, file, indent=4)