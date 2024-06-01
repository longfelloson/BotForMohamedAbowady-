from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message, User, InputFile, FSInputFile
from sqlalchemy.ext.asyncio import AsyncSession

from src import config
from src.subscriptions.crud import get_subscriptions, get_subscription
from src.subscriptions.files.utils import update_cvs_file
from src.subscriptions.keyboards import subscriptions_plans_keyboard
from src.subscriptions.schemas import SubscriptionTime, SubscriptionStatus
from src.subscriptions.utils import get_subscription_info

router = Router(name="Buttons")


@router.message(F.text == "Plans")
async def plans_button_handler(message: Message, user: User, session: AsyncSession):
    """
    "Plans" button's handler
    """
    user_subscriptions = await get_subscriptions(session, user_id=user.id, status=SubscriptionStatus.ACTIVE)
    max_active_subscriptions = [sub for sub in user_subscriptions if sub.subscription_time == SubscriptionTime.YEAR]
    if max_active_subscriptions:
        await message.reply(text="You have max subscription level 🤷‍♂️")
    else:
        await message.reply(
            text="Here are available subscription's plans ⤵️",
            reply_markup=subscriptions_plans_keyboard(user_subscriptions)
        )


@router.message(F.text == "Status")
async def status_button_handler(message: Message, user: User, session: AsyncSession):
    """
    "Status" button's handler
    """
    active_subscription = await get_subscription(user.id, session, status=SubscriptionStatus.ACTIVE)
    if not active_subscription:
        await message.reply("You don't have any active subscription 🤷‍♂️")
    else:
        await message.reply(get_subscription_info(active_subscription))


@router.message(F.text == "Report")
async def report_button_handler(message: Message, session: AsyncSession):
    """
    "Report" button's handler
    """
    subscriptions = await get_subscriptions(session)
    update_cvs_file(subscriptions)

    if subscriptions:
        await message.reply_document(FSInputFile(config.CVS_FILE_PATH), caption="Here is file with users ⤴️")
    else:
        await message.reply("File is empty 🤷‍♂️")
