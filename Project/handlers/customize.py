from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from database import get_player, save_player

router = Router()

# 🎖 Доступные титулы и рамки (можно расширить)
TITLES = {
    "⭐ Престиж": "⭐ Престиж",
    "👑 Донатер": "👑 Донатер"
}

FRAMES = {
    "💎": "💎",
    "🔥": "🔥",
    "✨": "✨"
}

@router.message(F.text == "/customize")
async def customize_menu(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏷 Выбрать титул", callback_data="custom_title")],
        [InlineKeyboardButton(text="💠 Выбрать рамку", callback_data="custom_frame")]
    ])
    await message.answer("🎨 Настрой свой профиль:", reply_markup=keyboard)

@router.callback_query(F.data == "custom_title")
async def choose_title_menu(call: CallbackQuery):
    keyboard = InlineKeyboardMarkup()
    for key in TITLES:
        keyboard.inline_keyboard.append([
            InlineKeyboardButton(text=key, callback_data=f"set_title:{key}")
        ])
    await call.message.edit_text("🏷 Выбери титул:", reply_markup=keyboard)

@router.callback_query(F.data == "custom_frame")
async def choose_frame_menu(call: CallbackQuery):
    keyboard = InlineKeyboardMarkup()
    for key in FRAMES:
        keyboard.inline_keyboard.append([
            InlineKeyboardButton(text=key, callback_data=f"set_frame:{key}")
        ])
    await call.message.edit_text("💠 Выбери рамку:", reply_markup=keyboard)

@router.callback_query(F.data.startswith("set_title:"))
async def set_title(call: CallbackQuery):
    title = call.data.split(":", 1)[1]
    user_id = str(call.from_user.id)
    player = await get_player(user_id)

    if not player:
        await call.message.edit_text("⚠️ Сначала используй /start.")
        return

    await save_player(
        user_id=user_id,
        username=player[1],
        resources=player[2],
        level=player[3],
        mine_level=player[4],
        inventory=player[5],
        minefield=player[6],
        daily_quest=player[7],
        last_quest_date=player[8],
        title=title,
        frame=player[10],
        donate_currency=player[12]
    )

    await call.message.edit_text(f"✅ Титул установлен: {title}")

@router.callback_query(F.data.startswith("set_frame:"))
async def set_frame(call: CallbackQuery):
    frame = call.data.split(":", 1)[1]
    user_id = str(call.from_user.id)
    player = await get_player(user_id)

    if not player:
        await call.message.edit_text("⚠️ Сначала используй /start.")
        return

    await save_player(
        user_id=user_id,
        username=player[1],
        resources=player[2],
        level=player[3],
        mine_level=player[4],
        inventory=player[5],
        minefield=player[6],
        daily_quest=player[7],
        last_quest_date=player[8],
        title=player[9],
        frame=frame,
        donate_currency=player[12]
    )

    await call.message.edit_text(f"✅ Рамка установлена: {frame}")
