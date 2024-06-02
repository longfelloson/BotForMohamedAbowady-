from aiogram.types import BotCommand
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from src import database
from src.app.loader import dp, bot
from src.app.middlewares import PayloadMiddleware
from src.app.routers.buttons import router as buttons_router
from src.app.routers.commands import router as commands_router
from src.app.routers.payments import router as payments_router
from src.app.routers.codes import router as codes_router
from src.subscriptions.utils import kick_expired

scheduler = AsyncIOScheduler()


async def set_commands() -> None:
    """
    Установка команд по умолчанию
    """
    commands = [
        BotCommand(command="/start", description="Command of starting the bot")
    ]
    await bot.set_my_commands(commands)


async def startup() -> None:
    """
    Starting the main processes for the bot
    """
    dp.include_routers(commands_router, buttons_router, payments_router, codes_router)
    dp.message.outer_middleware.register(PayloadMiddleware())
    dp.callback_query.outer_middleware.register(PayloadMiddleware())

    scheduler.add_job(kick_expired, trigger='interval', seconds=10)
    scheduler.start()

    await set_commands()
    await database.create_tables()
    await dp.start_polling(bot)
