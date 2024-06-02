from aiogram import Router, F
from aiogram.types import Message, User, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.filters import CodesFilter
from src.app.loader import bot
from src.subscriptions.codes.crud import create_code
from src.subscriptions.codes.keyboards import codes_keyboard
from src.users.crud import update_user
from src.subscriptions.codes import crud

router = Router(name="Codes")


@router.message(CodesFilter())
async def codes_handler(message: Message, user: User, session: AsyncSession):
    """
    Codes handler
    """
    await update_user(user.id, session, discount=True)
    await message.reply("You have successfully activated the discount ✅")


@router.callback_query(F.data == "create_code")
async def create_code_button_handler(call: CallbackQuery, user: User, session: AsyncSession):
    """
    View codes
    """
    await bot.answer_callback_query(call.id)
    await call.message.edit_text(f"New discount code: <b><code>{await create_code(session)}</code></b>")


@router.callback_query(F.data.regexp("view_codes"))
async def view_codes_button_handler(call: CallbackQuery, session: AsyncSession):
    """
    View codes
    """
    action = call.data.split("*")[1]
    codes = await crud.get_codes(session)

    await bot.answer_callback_query(call.id)
    await call.message.edit_text("Available codes ⤵️", reply_markup=codes_keyboard(codes, action))


@router.callback_query(F.data.regexp("delete_code"))
async def delete_code_button_handler(call: CallbackQuery, session: AsyncSession):
    """
    Deleting code by id
    """
    code_id = call.data.split("*")[1]

    await bot.answer_callback_query(call.id)
    await crud.delete_code(code_id, session)
    await call.message.edit_text("You have successfully deleted the code ✅")
