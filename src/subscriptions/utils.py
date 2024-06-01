from datetime import datetime, timedelta

from aiogram.types import ChatInviteLink
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy.ext.asyncio import AsyncSession

from src import config
from src.app.loader import bot
from src.database import get_async_session
from src.subscriptions import crud
from src.subscriptions.models import Subscription
from src.subscriptions.schemas import SubscriptionStatus, SubscriptionTime

CHANNEL_INVITE_LINK_MEMBER_LIMIT = 1


async def create_subscription(user_id: int, subscription_time: str, session: AsyncSession) -> ChatInviteLink:
    """
    Creating a subscription for user with given subscription time.
    """
    expires_at = get_expire_datetime_by_time(subscription_time)

    await crud.add_subscription(user_id, expires_at, subscription_time, session)
    await bot.unban_chat_member(config.CHANNEL_ID, user_id)
    invite_link = await bot.create_chat_invite_link(
        chat_id=config.CHANNEL_ID,
        member_limit=CHANNEL_INVITE_LINK_MEMBER_LIMIT,
        expire_date=expires_at
    )
    return invite_link


async def kick_expired() -> None:
    """
    Kick expired subscriptions.
    """
    async for session in get_async_session():
        subscriptions = await crud.get_subscriptions(
            session, type_=SubscriptionStatus.EXPIRED, status=SubscriptionStatus.ACTIVE
        )
        for expired_subscription in subscriptions:
            await crud.update_subscription(expired_subscription.user_id, session, status=SubscriptionStatus.EXPIRED)
            await bot.ban_chat_member(config.CHANNEL_ID, expired_subscription.user_id)


def get_expire_datetime_by_time(subscription_time: str) -> datetime:
    """
    Getting datetime by selected time
    """
    current_datetime = datetime.now()

    match subscription_time:
        case SubscriptionTime.WEEK:
            return current_datetime + timedelta(minutes=10)
        case SubscriptionTime.MONTH:
            return current_datetime + timedelta(weeks=4)
        case SubscriptionTime.YEAR:
            return current_datetime + timedelta(days=365)


def get_subscription_info(subscription: Subscription) -> dict:
    """
    Getting subscription information
    """
    sub_level = ""
    match subscription.subscription_time:
        case SubscriptionTime.WEEK:
            sub_level = "🥉"
        case SubscriptionTime.MONTH:
            sub_level = "🥈"
        case SubscriptionTime.YEAR:
            sub_level = "🥇"

    level = f"{sub_level} Level: <b>{subscription.subscription_time}</b>"
    expiration = f"⏳ Expiration: <b>{subscription.expires_at.strftime('%Y-%m-%d %H:%M')}</b>"

    return f"{level}\n\n{expiration}"


