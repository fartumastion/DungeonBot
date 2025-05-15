from aiogram import Router, F
from aiogram.types import Message
from database import get_player, save_player
from datetime import date
import random
import json

router = Router()

@router.message(F.text.in_(["🎯 Daily Quest", "/daily"]))
async def daily_quest_handler(message: Message):
    user_id = str(message.from_user.id)
    player = await get_player(user_id)

    if not player:
        await message.answer("⚠️ Сначала напиши /start.")
        return

    last_quest_date = player[8]
    today = date.today().isoformat()

    if last_quest_date == today:
        await message.answer("📆 Ты уже выполнял квест сегодня. Возвращайся завтра!")
        return

    reward = random.randint(2, 5)
    new_resources = player[2] + reward

    await save_player(
        user_id=user_id,
        username=player[1],
        resources=new_resources,
        level=player[3],
        mine_level=player[4],
        inventory=player[5],
        minefield=player[6],
        daily_quest="done",
        last_quest_date=today,
        title=player[9],
        frame=player[10],
        donate_currency=player[12]
    )

    await message.answer(f"🎁 Ты выполнил ежедневное задание и получил {reward} руды!")
