from aiogram.types import KeyboardButton as Button, ReplyKeyboardMarkup as Keyboard, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder as Builder

from src import config


def main_keyboard(user_id: int) -> Keyboard:
    """
    Keyboard with main button
    """
    builder = Builder().row(
        Button(text="Plans"), Button(text="Status")
    )
    if user_id == config.CHAT_OWNER_ID:
        builder.row(
            Button(text="Report")
        )
    return builder.as_markup(resize_keyboard=True)
