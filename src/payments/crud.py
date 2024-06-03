from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.payments.models import Payment


async def create_payment(
        user_id: int, amount: int, message_id: int,
        subscription_period: str, session: AsyncSession
) -> None:
    """
    Creates payment for database
    """
    await session.execute(insert(Payment).values(
        user_id=user_id, message_id=message_id, amount=amount, subscription_period=subscription_period)
    )
    await session.commit()


async def get_payment(id_: int, session: AsyncSession) -> Payment:
    """
    Returns payment from database
    """
    payment = await session.execute(select(Payment).where(Payment.id_ == id_))
    return payment.scalar_one()


async def update_payment(id_: int, session: AsyncSession, **values) -> None:
    """
    Updates payment in database
    """
    await session.execute(update(Payment).where(Payment.id_ == id_).values(**values))
    await session.commit()
