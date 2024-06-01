from aiogram.types import InlineKeyboardMarkup as InlineKeyboard, InlineKeyboardButton as InlineButton, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder as InlineBuilder

from src.payments.schemas import PaymentSchema


def payment_keyboard(payment: PaymentSchema, subscription_time: str) -> InlineKeyboard:
    """
    Keyboard with buttons for payment details
    """
    builder = InlineBuilder().row(InlineButton(
        text="Pay", web_app=WebAppInfo(url=payment.url)
    ))
    builder.row(InlineButton(
        text="Check", callback_data=f"check_payment*{payment.id_}*{subscription_time}"
    ))
    return builder.as_markup()
