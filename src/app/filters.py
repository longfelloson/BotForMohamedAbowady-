from aiogram.filters import BaseFilter
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from src.subscriptions.codes.crud import get_codes


class CodesFilter(BaseFilter):
    async def __call__(self, message: Message, session: AsyncSession):
        if message.text.isdigit():
            return int(message.text) in [code.code for code in await get_codes(session)]
        return False
