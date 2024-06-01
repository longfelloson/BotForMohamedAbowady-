from aiogram import Router, F
from aiogram.types import CallbackQuery, User
from sqlalchemy.ext.asyncio import AsyncSession

from src.payments.keyboards import payment_keyboard
from src.payments.utils import create_payment, check_payment
from src.subscriptions.keyboards import channel_invite_link_keyboard
from src.subscriptions.utils import create_subscription

router = Router(name="Payments")


@router.callback_query(F.data.regexp("create_payment"))
async def create_payment_button_handler(call: CallbackQuery):
    """

    """
    subscription_time = call.data.split("*")[1]
    payment = await create_payment()

    await call.message.edit_text(
        text="Payment link is below ⤵️", reply_markup=payment_keyboard(payment, subscription_time)
    )


@router.callback_query(F.data.regexp("check_payment"))
async def check_payment_button_handler(call: CallbackQuery, user: User, session: AsyncSession):
    """

    """
    payment_id, subscription_time = call.data.split("*")[1:]

    if await check_payment(payment_id):
        invite_link = await create_subscription(user.id, subscription_time, session)

        await call.message.edit_text(
            text="Congratulations, below is the link to the channel ⤵️",
            reply_markup=channel_invite_link_keyboard(invite_link.invite_link)
        )
    else:
        await call.answer("Payment is not payed 🤷‍♂️", show_alert=True)
