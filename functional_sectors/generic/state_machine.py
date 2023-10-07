from aiogram.dispatcher.filters.state import StatesGroup
from ..message_to_ok.states import MTKStates

class FSMClient(MTKStates, StatesGroup):
    pass
    # anonim_msg_text = State()

    # sos_confirmation = State()

    # new_post_text = State()
    # new_post_headline = State()
    # new_post_picture = State()