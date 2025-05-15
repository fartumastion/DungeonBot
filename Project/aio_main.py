import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

# Инициализация БД
from database import init_db
from config import load_config

# Роутеры
from handlers.start import router as start_router
from handlers.mine import router as mine_router
from handlers.inventory import router as inventory_router
from handlers.top import router as top_router
from handlers.daily import router as daily_router
from handlers.help import router as help_router
from handlers.gold_bonus import router as gold_router
from handlers.prestige import router as prestige_router
from handlers.customize import router as customize_router
from donate_aio_stars import router as donate_router

async def main():
    config = load_config()
    await init_db()  # 🔄 Асинхронная инициализация базы

    from aiogram.client.default import DefaultBotProperties

    bot = Bot(
        token=config.bot_token,
        default=DefaultBotProperties(parse_mode="HTML")
    )

    dp = Dispatcher(storage=MemoryStorage())

    # Подключаем все роутеры
    dp.include_router(start_router)
    dp.include_router(mine_router)
    dp.include_router(inventory_router)
    dp.include_router(top_router)
    dp.include_router(daily_router)
    dp.include_router(help_router)
    dp.include_router(gold_router)
    dp.include_router(prestige_router)
    dp.include_router(donate_router)
    dp.include_router(customize_router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
