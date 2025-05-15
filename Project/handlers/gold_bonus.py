from aiogram import Router, F
from aiogram.types import Message
from database import get_player, save_player
import random
import json

router = Router()

@router.message(F.text == "💠 Bonus Mine")
async def bonus_mine_handler(message: Message):
    user_id = str(message.from_user.id)
    player = await get_player(user_id)

    if not player:
        await message.answer("⚠️ Сначала используй /start.")
        return

    mine_level = player[4]
    if mine_level < 100:
        await message.answer("🔒 Бонусная шахта открывается с 100 уровня.")
        return

    resources = player[2]
    bonus = random.randint(3, 7)
    resources += bonus

    await save_player(
        user_id=user_id,
        username=player[1],
        resources=resources,
        level=player[3],
        mine_level=mine_level,
        inventory=player[5],
        minefield=player[6],
        daily_quest=player[7],
        last_quest_date=player[8],
        title=player[9],
        frame=player[10],
        donate_currency=player[12]
    )

    await message.answer(f"💠 Ты нашёл {bonus} бонусной руды!")

@router.message(F.text == "🏵 Gold Mine")
async def gold_mine_handler(message: Message):
    user_id = str(message.from_user.id)
    player = await get_player(user_id)

    if not player:
        await message.answer("⚠️ Сначала используй /start.")
        return

    inventory = json.loads(player[5]) if player[5] else []

    if "🎫 Золотой билет" not in inventory:
        await message.answer("🚫 У тебя нет 🎫 Золотого билета для входа в золотую шахту.")
        return

    inventory.remove("🎫 Золотой билет")
    resources = player[2] + random.randint(5, 10)

    await save_player(
        user_id=user_id,
        username=player[1],
        resources=resources,
        level=player[3],
        mine_level=player[4],
        inventory=json.dumps(inventory),
        minefield=player[6],
        daily_quest=player[7],
        last_quest_date=player[8],
        title=player[9],
        frame=player[10],
        donate_currency=player[12]
    )

    await message.answer("🏵 Ты обменял 🎫 Золотой билет и добыл ценную руду!")
