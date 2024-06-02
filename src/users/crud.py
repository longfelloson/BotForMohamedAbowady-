from typing import Optional

from sqlalchemy import insert, select, update, and_
from sqlalchemy.ext.asyncio import AsyncSession

from src.users.models import User


async def create_user(user_id: int, session: AsyncSession) -> None:
    """
    Creates new user
    """
    await session.execute(insert(User).values(id_=user_id))
    await session.commit()


async def get_user(user_id: int, session: AsyncSession) -> Optional[User]:
    """
    Gets user if it exists
    """
    user = await session.execute(select(User).where(User.id_ == user_id))
    return user.scalar_one_or_none()


async def update_user(user_id: int, session: AsyncSession, **fields) -> None:
    """
    Updates user
    """
    await session.execute(update(User).where(User.id_ == user_id).values(**fields))
    await session.commit()
