from sqlite3 import connect as connect_lite
from os import mkdir, path

path = path.abspath(__file__)[:path.abspath(__file__).rindex('\\')]

def create_database():
    '''Создание таблиц'''
    try:
        mkdir(path + '/database')
    except FileExistsError:
        pass
    with connect_lite(path + '/database/db_msg_to_ok.sql') as conn:
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS coulddawn (user_id int PRIMARY KEY, time_end_cd int)")
        cur.execute("CREATE TABLE IF NOT EXISTS messages (msg_id int PRIMARY KEY, user_id int)")
        conn.commit()