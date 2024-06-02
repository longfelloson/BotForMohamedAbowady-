from datetime import datetime

from aiogram import Router, F
from aiogram.types import CallbackQuery, User
from fastapi import APIRouter, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.loader import bot
from src.database import get_async_session
from src.payments import crud
from src.payments.crud import create_payment
from src.payments.keyboards import payment_keyboard
from src.payments.schemas import PaymentStatus
from src.payments.utils import get_payment
from src.subscriptions.keyboards import channel_invite_link_keyboard
from src.subscriptions.utils import create_subscription

router = Router(name="Payments")
web_router = APIRouter()

PAID_PAYMENT_STATUS = "CAPTURED"


@router.callback_query(F.data.regexp("create_payment"))
async def create_payment_button_handler(call: CallbackQuery, user: User, session: AsyncSession):
    """
    Create payment button
    """
    subscription_period, amount = call.data.split("*")[1:]
    payment_schema = await get_payment(amount)

    await create_payment(user.id, amount, call.message.message_id, subscription_period, session)
    await call.message.edit_text(
        text="Payment link is below ⤵️", reply_markup=payment_keyboard(payment_schema, subscription_period)
    )


# @router.callback_query(F.data.regexp("check_payment"))
# async def check_payment_button_handler(call: CallbackQuery, user: User, session: AsyncSession):
#     """
#     Check payment button
#     """
#     payment_id, subscription_time = call.data.split("*")[1:]
#
#     if await check_payment(payment_id):
#         invite_link = await create_subscription(user.id, subscription_time, session)
#
#         await call.message.edit_text(
#             text="Congratulations, below is the link to the channel ⤵️",
#             reply_markup=channel_invite_link_keyboard(invite_link.invite_link)
#         )
#     else:
#         await call.answer("Payment is not paid 🤷‍♂️", show_alert=True)


@web_router.post('/payment')
async def post_request_handler(request: Request, session: AsyncSession = Depends(get_async_session)):
    """
    This endpoint will send a successful payment request.
    """
    data = await request.json()
    if data['status'] == PAID_PAYMENT_STATUS:
        payment = await crud.get_payment(data['payment_id'], session)
        invite_link = await create_subscription(payment.id_, payment.subscription_period, session)

        await crud.update_payment(payment.id_, session, status=PaymentStatus.PAID, paid_at=datetime.now())
        await bot.edit_message_text(
            text="Congratulations, below is the link to the channel ⤵️",
            chat_id=payment.user_id,
            message_id=payment.message_id,
            reply_markup=channel_invite_link_keyboard(invite_link.invite_link)
        )
