from typing import Any, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message

from src.database import get_async_session


class PayloadMiddleware(BaseMiddleware):
    """
    The middleware of the payload that transmits the object of the database session and the user
    """
    async def __call__(self, handler, message: Message, data: Dict[str, Any]) -> Any:
        async for session in get_async_session():
            data['session'] = session
            data['user'] = message.from_user

            return await handler(message, data)
