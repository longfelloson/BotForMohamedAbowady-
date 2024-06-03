from typing import List

from aiogram.types import InlineKeyboardButton as InlineButton, InlineKeyboardMarkup as InlineKeyboard
from aiogram.utils.keyboard import InlineKeyboardBuilder as InlineBuilder

from src.subscriptions.codes.models import Code


def codes_management_menu_keyboard() -> InlineKeyboard:
    """
    Codes management menu keyboard
    """
    builder = InlineBuilder().row(InlineButton(
        text="🔨 Create code", callback_data="create_code"
    ))
    builder.row(InlineButton(
        text="🚮 Delete code", callback_data="view_codes*delete"
    ))
    return builder.as_markup()


def codes_keyboard(codes: List[Code], action: str) -> InlineKeyboard:
    """
    Codes keyboard
    """
    buttons = [
        InlineButton(text=f"{code.id_}. {code.code}", callback_data=f"{action}_code*{code.id_}") for code in codes
    ]
    return InlineBuilder().add(*buttons).adjust(1).as_markup()
