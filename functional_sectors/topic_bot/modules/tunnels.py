'''Модуль для удобного взаимодействия с БД тоннелей'''
import sqlite3
class Tunnels:
    
    def __init_tunnels_table(self):
        self.cursor.execute("""
        create table if not exists tunnels
        (
            id integer primary key autoincrement,
            topic_chat_id integer,
            topic_id integer,
            freelance_chat_id integer unique
        )""")
    def __init__(self,dbPath="tunnels.db"):
        self.db_path=dbPath
        self.__launch_db()
        self.__init_tunnels_table()
    def __reboot_db(self):
        self.dispose()
        self.__launch_db()
    def __launch_db(self):
        self.db_connection=sqlite3.connect(self.db_path)
        self.cursor=self.db_connection.cursor()
    
    def init_tunnel(self,topic_chat_id:int,topic_id:int)->int:
        self.cursor.execute(f"""
            insert into tunnels (topic_chat_id,topic_id,freelance_chat_id)
            values({topic_chat_id},{topic_id},null)
        """)
        self.__reboot_db()
        id=self.get_tunnel_id(topic_chat_id,topic_id)
        return id
    def get_freelance_chat(self,topic_chat_id:int,topic_id:int)->(int|None):
        self.cursor.execute(f"""
            select freelance_chat_id from tunnels 
            where topic_chat_id={topic_chat_id} and topic_id={topic_id}
        """)
        answer=self.cursor.fetchone()
        if(answer==None):
            return None
        freelance_chat_id=answer[0]
        return freelance_chat_id   
    def get_root_chat(self,freelance_chat):
        self.cursor.execute(f'''
            select topic_chat_id, topic_id from tunnels
            where freelance_chat_id={freelance_chat}
        ''')
        answer=self.cursor.fetchall()
        if(answer==None):
            return None
        return answer[0]
    def connect_to_tunnel(self,tunnel_id:int,freelance_id:int):
        self.cursor.execute(f"""
            update tunnels
            set freelance_chat_id = {freelance_id}
            where id={tunnel_id}
        """)
        self.__reboot_db()
    def __get_req_by_freelance_id(self,fl_id):
        return f"""
            select id from tunnels 
            where freelance_chat_id={fl_id}
        """
    def __get_req_by_topic_id(self,chat_id,topic_id):
        return f"""
            select id from tunnels 
            where topic_chat_id={chat_id} and topic_id={topic_id}
        """
    def get_tunnel_id(self,chat_id,topic_id:int|None)->(int|None):
        cmd=None
        if topic_id==None:
            cmd=self.__get_req_by_freelance_id(chat_id)
        else:
            cmd=self.__get_req_by_topic_id(chat_id,topic_id)
        self.cursor.execute(cmd)
        answer=self.cursor.fetchone()
        if(answer==None):
            return None
        chat_id=answer[0]
        return chat_id   
    
    def tunnel_employing(self,tunnel_id:int)->bool:
        self.cursor.execute(f"""
            select id from tunnels
            where id={tunnel_id} and freelance_chat_id not null
        """)
        response=self.cursor.fetchone()
        return response!=None and response[0]!=None
    def tunnel_exists(self,tunnel_id:int)->bool:
        self.cursor.execute(f"""
            select id from tunnels
            where id={tunnel_id}
        """)
        response=self.cursor.fetchone()
        return response!=None and response[0]!=None

    def chat_hasnt_connection(self,bindable_chat:int)->bool:
        self.cursor.execute(f"""
            select id from tunnels
            where freelance_chat_id={bindable_chat}
        """)
        answer=self.cursor.fetchone()
        return answer==None or answer[0]==None
    
    def destroy_tunnel(self,tunnel_id:int):
        self.cursor.execute(f"""
            delete from tunnels
            where id={tunnel_id}
        """)
        self.__reboot_db()
    def dispose(self):
        self.db_connection.commit()
        self.db_connection.close()
