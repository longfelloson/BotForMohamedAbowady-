from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message, User
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.keyboards import main_keyboard
from src.users.crud import get_user, create_user

router = Router(name="Commands")


@router.message(CommandStart())
async def start_command_handler(message: Message, user: User, session: AsyncSession):
    """
    This handler will be called when a command is started.
    """
    if not await get_user(user.id, session):
        await create_user(user.id, session)

    await message.reply(text="Hello!", reply_markup=main_keyboard(user.id))
