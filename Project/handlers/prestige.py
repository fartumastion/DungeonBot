from aiogram import Router, F
from aiogram.types import Message
from database import get_player, save_player
import json

router = Router()

@router.message(F.text == "/prestige")
async def prestige_handler(message: Message):
    user_id = str(message.from_user.id)
    player = await get_player(user_id)

    if not player:
        await message.answer("⚠️ Сначала напиши /start.")
        return

    mine_level = player[4]
    if mine_level < 100:
        await message.answer("🔒 Престиж доступен только с 100 уровня.")
        return

    # Сброс прогресса и выдача титула
    await save_player(
        user_id=user_id,
        username=player[1],
        resources=0,
        level=1,
        mine_level=1,
        inventory=json.dumps([]),
        minefield=json.dumps([]),
        daily_quest="",
        last_quest_date="",
        title="⭐ Престиж",
        frame=player[10],
        donate_currency=player[12]
    )

    await message.answer("🌟 Престиж активирован! Прогресс сброшен, но ты получил титул ⭐ Престиж.")
