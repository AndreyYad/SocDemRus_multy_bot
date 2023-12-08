from aiogram.fsm.state import StatesGroup, State

class FSMClient(StatesGroup):
    anonim_msg_text = State()

    sos_confirmation = State()

    new_post_text = State()
    new_post_headline = State()
    new_post_picture = State()