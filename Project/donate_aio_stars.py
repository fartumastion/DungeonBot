from aiogram import Router, F
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery, SuccessfulPayment
from aiogram.types.message import ContentType
from database import get_player, save_player

router = Router()

# 🔐 MOCK-токен для тестов (можно заменить на STARS:... позже)
PROVIDER_TOKEN = "381764678:TEST:65313"
CURRENCY = "RUB"

# 💎 Команда для покупки кристаллов (тест через mock)
@router.message(F.text == "/buy_crystals")
async def cmd_buy_crystals(message: Message):
    prices = [LabeledPrice(label="10 кристаллов", amount=10000)]  # 100.00 RUB (тестовая сумма)
    await message.answer_invoice(
        title="Покупка кристаллов",
        description="10 кристаллов в тестовом режиме",
        provider_token=PROVIDER_TOKEN,
        currency=CURRENCY,
        prices=prices,
        start_parameter="buy_crystals",
        payload="crystals_10"
    )

# ✅ Подтверждение перед оплатой
@router.pre_checkout_query()
async def process_pre_checkout(pre_checkout_query: PreCheckoutQuery):
    await pre_checkout_query.answer(ok=True)

# 🧾 Успешная оплата
@router.message(F.content_type == ContentType.SUCCESSFUL_PAYMENT)
async def process_successful_payment(message: Message):
    user_id = str(message.from_user.id)
    row = get_player(user_id)

    if not row:
        await message.answer("⚠️ Ты не зарегистрирован. Используй /start в основном боте.")
        return

    donate_currency = row[12] if len(row) > 12 else 0

    if message.successful_payment.invoice_payload == "crystals_10":
        donate_currency += 10

    save_player(
        user_id=user_id,
        username=row[1],
        resources=row[2],
        level=row[3],
        mine_level=row[4],
        inventory=row[5],
        minefield=row[6],
        daily_quest=row[7],
        last_quest_date=row[8],
        title=row[9] if len(row) > 9 else "",
        frame=row[10] if len(row) > 10 else "",
        donate_currency=donate_currency
    )

    await message.answer("✅ Оплата успешна! Тебе начислено 10 💎 кристаллов.")
