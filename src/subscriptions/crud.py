from datetime import datetime
from typing import List, Optional

from sqlalchemy import select, update, insert, and_
from sqlalchemy.ext.asyncio import AsyncSession

from src import config
from src.subscriptions.models import Subscription
from src.subscriptions.schemas import SubscriptionStatus


async def add_subscription(
        user_id: int, expires_at: datetime,
        subscription_time: str, session: AsyncSession
) -> None:
    """
    Adding new subscription to database
    """
    await session.execute(insert(Subscription).values(
        user_id=user_id, expires_at=expires_at, subscription_time=subscription_time)
    )
    await session.commit()


async def get_subscription(user_id: int, session: AsyncSession, **fields) -> Optional[Subscription]:
    """
    Get a subscription of user on user id
    """
    stmt = select(Subscription).where(Subscription.user_id == user_id)
    if fields:
        filters = [getattr(Subscription, key) == value for key, value in fields.items()]
        stmt = stmt.where(and_(*filters))

    subscription = await session.execute(stmt)
    return subscription.scalar_one_or_none()


async def update_subscription(user_id: int, session: AsyncSession, **fields) -> None:
    """
    Update a subscription of user on user id
    """
    await session.execute(update(Subscription).where(Subscription.user_id == user_id).values(**fields))
    await session.commit()


async def get_subscriptions(session: AsyncSession, type_: str = "All", **fields) -> List[Subscription]:
    """
    Get all subscriptions
    """
    stmt = select(Subscription).where(Subscription.user_id != config.CHAT_OWNER_ID)
    current_datetime = datetime.now()

    if type_ == SubscriptionStatus.EXPIRED:
        stmt = stmt.where(Subscription.expires_at < current_datetime)
    elif type_ == SubscriptionStatus.ACTIVE:
        stmt = stmt.where(Subscription.expires_at > current_datetime)

    if fields:
        filters = [getattr(Subscription, key) == value for key, value in fields.items()]
        stmt = stmt.where(and_(*filters))

    subscriptions = await session.execute(stmt)
    return subscriptions.scalars().all()
