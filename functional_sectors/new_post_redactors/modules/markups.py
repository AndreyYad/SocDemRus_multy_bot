from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

# callback_id = 1

async def markup_like():
    '''Inline-кнопки установки и отмены лайка под предложенным постом'''
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(text='👍🏻', callback_data='1_like'),
        InlineKeyboardButton(text='↩️', callback_data='1_remove_like')
    )

    return builder.as_markup()