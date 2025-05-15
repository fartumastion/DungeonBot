from aiogram import Router, F
from aiogram.types import Message
from database import get_top_players

router = Router()

@router.message(F.text.in_(["🏆 Top", "/top"]))
async def top_handler(message: Message):
    players = await get_top_players()

    if not players:
        await message.answer("🏆 Пока что никого нет в топе.")
        return

    text = "🏆 <b>Топ игроков:</b>\n\n"
    for i, player in enumerate(players, 1):
        user_id, username, resources, level, mine_level, title, frame, donate_currency = player
        title = title or ""
        frame = frame or ""
        text += f"{i}. {frame}@{username}{frame} — {title} | 🏔 {mine_level} ур., 💰 {resources} руды\n"

    await message.answer(text)
