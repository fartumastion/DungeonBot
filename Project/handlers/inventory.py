from aiogram import Router, F
from aiogram.types import Message
from database import get_player
import json

router = Router()

@router.message(F.text.in_(["📦 Inventory", "/inventory"]))
async def inventory_handler(message: Message):
    user_id = str(message.from_user.id)
    player = await get_player(user_id)

    if not player:
        await message.answer("⚠️ Ты не зарегистрирован. Напиши /start.")
        return

    username = player[1]
    resources = player[2]
    mine_level = player[4]
    inventory = json.loads(player[5]) if player[5] else []
    title = player[9] or ""
    frame = player[10] or ""
    donate_currency = player[12] if len(player) > 12 else 0

    items = "\n".join(f"• {item}" for item in inventory) if inventory else "Пусто 🎒"

    text = (
        f"{frame}@{username}{frame}\n"
        f"{title + ' ' if title else ''}💰 Руда: {resources}\n"
        f"💎 Кристаллы: {donate_currency}\n"
        f"⛏ Уровень шахты: {mine_level}\n\n"
        f"🎒 Инвентарь:\n{items}"
    )

    await message.answer(text)
