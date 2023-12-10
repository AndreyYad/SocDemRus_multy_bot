from sqlite3 import connect
from os import mkdir, path

path = path.abspath(__file__)[:path.abspath(__file__).rindex('/')]

def create_database_new_post_redactors():
    '''Создание таблиц'''
    try:
        mkdir(path + '/database')
    except FileExistsError:
        pass
    with connect(path + '/database/db_new_post.sql') as conn:
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS new_post (post_id INTEGER PRIMARY KEY AUTOINCREMENT, msg_id int, user_id int, text_post text, headline_post varchar(200), picture_post varchar(150), time_repost int)")
        cur.execute("CREATE TABLE IF NOT EXISTS likes (post_id int, user_id int)")
        conn.commit()