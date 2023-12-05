from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

async def markup_like():
    '''Inline-кнопки установки и отмены лайка под предложенным постом'''
    markup = InlineKeyboardMarkup()

    markup.row(
        InlineKeyboardButton('👍🏻', callback_data='like'),
        InlineKeyboardButton('↩️', callback_data='remove_like')
    )

    return markup