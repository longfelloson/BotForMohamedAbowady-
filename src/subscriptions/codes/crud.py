from random import randint
from typing import List

from sqlalchemy import insert, delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.subscriptions.codes.models import Code


async def create_code(session: AsyncSession) -> int:
    """
    Creates new code for subscription's discount
    """
    code = randint(1111111111, 9999999999)

    await session.execute(insert(Code).values(code=code))
    await session.commit()

    return code


async def delete_code(code_id: int, session: AsyncSession) -> None:
    """
    Deletes existing code for subscription's discount
    """
    await session.execute(delete(Code).where(Code.id_ == code_id))
    await session.commit()


async def get_codes(session: AsyncSession) -> List[Code]:
    """
    Getting all codes for subscription's discount
    """
    codes = await session.execute(select(Code))
    return codes.scalars().all()
