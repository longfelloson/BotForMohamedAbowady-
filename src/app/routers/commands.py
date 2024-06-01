from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message, User

from src.app.keyboards import main_keyboard

router = Router(name="Commands")


@router.message(CommandStart())
async def start_command_handler(message: Message, user: User):
    """
    This handler will be called when a command is started.
    """
    await message.reply(text="Hello!", reply_markup=main_keyboard(user.id))
