from aiogram.dispatcher.filters.state import State, StatesGroup

class FSMClient(StatesGroup):
    anonim_msg_text = State()

    sos_confirmation_1 = State()
    sos_confirmation_2 = State()

    new_post_text = State()
    new_post_headline = State()
    new_post_picture = State()