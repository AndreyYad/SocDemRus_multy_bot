from aiogram.dispatcher.filters.state import StatesGroup, State

class States(StatesGroup):
    new_post_text = State()
    new_post_headline = State()
    new_post_picture = State()