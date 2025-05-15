from aiogram import Router, F
from aiogram.types import Message

router = Router()

@router.message(F.text.in_(["ℹ️ Help", "/help"]))
async def help_handler(message: Message):
    text = (
        "ℹ️ <b>Помощь по DungeonMine</b>\n\n"
        "⛏ <b>Mine</b> — копать руду\n"
        "📦 <b>Inventory</b> — посмотреть инвентарь\n"
        "🏆 <b>Top</b> — топ игроков по уровню шахты\n"
        "🎯 <b>Daily Quest</b> — ежедневная награда\n"
        "💠 <b>Bonus Mine</b> — открывается с 100 уровня\n"
        "🏵 <b>Gold Mine</b> — доступна при наличии Золотого билета\n"
        "🛍 <b>Donate Shop</b> — покупка титулов и рамок\n"
        "💎 <b>/buy_crystals</b> — покупка кристаллов (донат)\n"
        "⭐ <b>/prestige</b> — сброс прогресса ради титула\n"
        "\n"
        "🤖 Разработчик: @YourUsername"
    )
    await message.answer(text)
