from typing import List

from aiogram.types import InlineKeyboardButton as InlineButton, InlineKeyboardMarkup as InlineKeyboard
from aiogram.utils.keyboard import InlineKeyboardBuilder as InlineBuilder

from src.subscriptions.models import Subscription
from src.subscriptions.schemas import SubscriptionTime
from src.subscriptions.utils import get_price
from src.users.models import User


def subscriptions_plans_keyboard(user: User, user_subscriptions: List[Subscription]) -> InlineKeyboard:
    """
    Buttons for subscriptions plans keyboard
    """
    three_months_price = get_price(user, SubscriptionTime.THREE_MONTHS)
    month_price = get_price(user, SubscriptionTime.MONTH)
    buttons = {
        SubscriptionTime.MONTH:
            InlineButton(
                text=f"🥉 Subscription for month: ${month_price}",
                callback_data=f"create_payment*{SubscriptionTime.MONTH}*{month_price}"
            ),
        SubscriptionTime.THREE_MONTHS:
            InlineButton(
                text=f"🥈 Subscription for three months: ${three_months_price}",
                callback_data=f"create_payment*{SubscriptionTime.THREE_MONTHS}*{three_months_price}"
            )
    }
    user_subscriptions_times = [subscription.subscription_time for subscription in user_subscriptions]
    buttons_for_view = [buttons[time] for time in buttons if time not in user_subscriptions_times]
    return InlineBuilder().add(*buttons_for_view).adjust(1).as_markup()


def channel_invite_link_keyboard(link: str) -> InlineKeyboard:
    """
    Button for channel invite link
    """
    builder = InlineBuilder().add(InlineButton(
        text="Channel's Invite Link", url=link
    ))
    return builder.as_markup()
