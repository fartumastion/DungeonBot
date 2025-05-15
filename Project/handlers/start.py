from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from database import get_player, save_player
import json

router = Router()

main_menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="⛏ Mine"), KeyboardButton(text="📦 Inventory")
        ],
        [
            KeyboardButton(text="🏆 Top"), KeyboardButton(text="ℹ️ Help")
        ],
        [
            KeyboardButton(text="🏵 Gold Mine"), KeyboardButton(text="💠 Bonus Mine"),
            KeyboardButton(text="🎯 Daily Quest")
        ],
        [
            KeyboardButton(text="🛍 Donate Shop")
        ]
    ],
    resize_keyboard=True
)


@router.message(F.text == "/start")
async def start(message: Message):
    user_id = str(message.from_user.id)
    username = message.from_user.username or message.from_user.full_name

    player = await get_player(user_id)
    if not player:
        await save_player(
            user_id=user_id,
            username=username,
            resources=0,
            level=1,
            mine_level=1,
            inventory=json.dumps([]),
            minefield=json.dumps([])
        )

    await message.answer(
        "👋 Добро пожаловать в DungeonMine!\nГотов к шахтёрским приключениям?",
        reply_markup=main_menu_keyboard
    )
