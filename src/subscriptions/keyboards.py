from typing import List

from aiogram.types import InlineKeyboardButton as InlineButton, InlineKeyboardMarkup as InlineKeyboard, \
    InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder as InlineBuilder

from src.subscriptions.models import Subscription
from src.subscriptions.schemas import SubscriptionTime


def subscriptions_plans_keyboard(user_subscriptions: List[Subscription]) -> InlineKeyboard:
    """
    Buttons for subscriptions plans keyboard
    """
    buttons = {
        SubscriptionTime.WEEK:
            InlineButton(
                text="🥉 Subscription for week", callback_data=f"create_payment*{SubscriptionTime.WEEK}"
            ),
        SubscriptionTime.MONTH:
            InlineButton(
                text="🥈 Subscription for month", callback_data=f"create_payment*{SubscriptionTime.MONTH}"
            ),
        SubscriptionTime.YEAR:
            InlineButton(
                text="🥇 Subscription for year", callback_data=f"create_payment*{SubscriptionTime.YEAR}"
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
