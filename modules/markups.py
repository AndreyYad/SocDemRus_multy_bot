from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

async def markup_start():
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton('Что предлагает «Яблоко»', callback_data='party_program_select'),
        InlineKeyboardButton('Мой кандидат по округу', callback_data='my_candidate_address')
    )

    return markup