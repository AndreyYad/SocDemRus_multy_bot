from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

# callback_id = 2

async def markup_new_vk_post():
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(text='Отправить сейчас', callback_data='2_send_now'),
        InlineKeyboardButton(text='Отменить отправку', callback_data='2_cancel_send')
    )
    builder.row(
        InlineKeyboardButton(text='Изменить текст', callback_data='2_red_text')
    )

    return builder.as_markup()