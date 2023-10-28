from aiogram.dispatcher.filters.state import StatesGroup
from .imports import get_states

class FSMClient(*get_states(), StatesGroup):
    pass
    # anonim_msg_text = State()

    # sos_confirmation = State()

    # new_post_text = State()
    # new_post_headline = State()
    # new_post_picture = State()