from aiogram.types import Message

from .database.tunnels import Tunnels
from ..generic.messages import MESSAGES
from main_modules.bot_cmds import *

class topic_signalbot:

    def __init__(self):
        self.__tunnels = Tunnels()

    def __get_topic_id(self, msg: Message):
        return msg.message_thread_id

    async def init_tunnel(self, msg: Message):
        topic_id = self.__get_topic_id(msg)
        chat_id = msg.chat.id
        tunnels = self.__tunnels
        if topic_id != None:
            tunnel_id = tunnels.get_tunnel_id(chat_id,topic_id)
            if tunnel_id == None:
                tunnel_id = tunnels.init_tunnel(chat_id,topic_id)
                text = MESSAGES['init_tunnel'].format(tunnel_id)
            else:
                text = f"Тунель уже существует\nId: <code>{tunnel_id}</code>"
            await send_to_topic(text,chat_id,topic_id)
        else:
            await send_msg(chat_id,"Тунель может быть инициализирован только в треде (топике) и только членом СДР!")

    def __get_tunnel_id(self,args: str):
        try:
            _args = args.replace(" ","")
            return int(_args)
        except:
            return None
        
    async def connect_to_tunnel(self, msg: Message):
        chat_id = msg.chat.id
        args = msg.get_args()
        tunnels = self.__tunnels
        hasnt_connection = tunnels.chat_hasnt_connection(chat_id)
        if hasnt_connection:
            tunnel_id = self.__get_tunnel_id(args)
            if tunnel_id != None:
                tunnel_exists = tunnels.tunnel_exists(tunnel_id)
                if tunnel_exists:
                    tunnel_employing = tunnels.tunnel_employing(tunnel_id)
                    if not tunnel_employing:
                        tunnels.connect_to_tunnel(tunnel_id,chat_id)
                        text = MESSAGES["bind"]
                    else:
                        text = "Тоннель уже используется другим чатом!"
                else:
                    text = "Указываемого тунеля не существует!"
            else:
                text = "Некорректный id тунеля. Он должен быть представлен в числовом формате.\nПожалуйста, введите ещё раз"
        else:
            text = "Чат уже привязан!"
        await send_msg(chat_id,text)

    async def process_any_msg(self, msg: Message):
        chat_id = msg.chat.id
        topic_id = self.__get_topic_id(msg)
        tunnels = self.__tunnels

        if topic_id == None:
            distance = tunnels.get_root_chat(chat_id)
        else:
            distance = tunnels.get_freelance_chat(chat_id,topic_id)
        if isinstance(distance,tuple):
            (dist_chat_id, dist_topic_id) = distance
        else:
            dist_chat_id = distance
            dist_topic_id = None

        if dist_chat_id != None:
            await msg.forward(dist_chat_id,dist_topic_id)