from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

main = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="добавить", callback_data="add")],
        [InlineKeyboardButton(text="получить", callback_data="get")],
        [InlineKeyboardButton(text="показать все", callback_data="list")],
    ]
)
