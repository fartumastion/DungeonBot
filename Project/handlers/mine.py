from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from database import get_player, save_player
import json
import random
import time

router = Router()

# Константы для типов клеток
HIDDEN = "⬛"  # Скрытая клетка
EMPTY = "⬜"
ORE = "⛏"
DIAMOND = "💎"
LOOT_BOX = "🎁"
CAVE_IN = "💥"

# Константы для комбо
COMBO_TIMES = {
    1: 30,  # 30 секунд для 1 уровня
    2: 35,  # 35 секунд для 2 уровня
    3: 40,  # 40 секунд для 3 уровня
    4: 45,  # 45 секунд для 4 уровня
    5: 50,  # 50 секунд для 5 уровня
}

COMBO_MULTIPLIERS = {
    1: 1.5,  # x1.5 для 1 уровня
    2: 2.0,  # x2.0 для 2 уровня
    3: 2.5,  # x2.5 для 3 уровня
    4: 3.0,  # x3.0 для 4 уровня
    5: 4.0,  # x4.0 для 5 уровня
}

# Создание пустого поля 5x5
def create_empty_field():
    return [[HIDDEN for _ in range(5)] for _ in range(5)]

# Генерация случайного поля с учетом уровня
def generate_field(level):
    field = create_empty_field()
    # Распределение вероятностей для разных типов клеток с учетом уровня
    base_probabilities = {
        EMPTY: 0.4,    # 40% пустых клеток
        ORE: 0.3,      # 30% руды
        DIAMOND: 0.1,  # 10% алмазов
        LOOT_BOX: 0.1, # 10% лут-боксов
        CAVE_IN: 0.1   # 10% обвалов
    }
    
    # Увеличиваем шансы на редкие предметы с каждым уровнем
    level_bonus = min(level * 0.02, 0.2)  # Максимальный бонус 20%
    probabilities = {
        EMPTY: base_probabilities[EMPTY] - level_bonus,
        ORE: base_probabilities[ORE],
        DIAMOND: base_probabilities[DIAMOND] + level_bonus * 0.5,
        LOOT_BOX: base_probabilities[LOOT_BOX] + level_bonus * 0.3,
        CAVE_IN: base_probabilities[CAVE_IN] + level_bonus * 0.2
    }
    
    # Создаем два поля: одно для отображения, другое для хранения реальных значений
    display_field = create_empty_field()
    real_field = [[EMPTY for _ in range(5)] for _ in range(5)]
    
    for i in range(5):
        for j in range(5):
            r = random.random()
            cumulative = 0
            for cell_type, prob in probabilities.items():
                cumulative += prob
                if r <= cumulative:
                    real_field[i][j] = cell_type
                    break
    
    return display_field, real_field

# Создание клавиатуры из поля
def create_keyboard(display_field, real_field):
    keyboard = []
    for i in range(5):
        keyboard_row = []
        for j in range(5):
            # Для каждой кнопки храним и отображаемое значение, и реальное
            display_value = display_field[i][j]
            real_value = real_field[i][j]
            keyboard_row.append(InlineKeyboardButton(
                text=display_value,
                callback_data=f"mine_{i}_{j}_{real_value}"
            ))
        keyboard.append(keyboard_row)
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

# Проверка, все ли клетки открыты
def is_field_completed(display_field):
    return all(cell != HIDDEN for row in display_field for cell in row)

@router.message(F.text == "⛏ Mine")
async def mine_handler(message: Message):
    user_id = str(message.from_user.id)
    player = await get_player(user_id)

    if not player:
        await message.answer("⚠️ Сначала используй /start.")
        return

    # Генерируем новое поле с учетом уровня
    display_field, real_field = generate_field(player[4])  # player[4] - это mine_level
    
    # Сохраняем поля в базе данных
    await save_player(
        user_id=user_id,
        username=player[1],
        resources=player[2],
        level=player[3],
        mine_level=player[4],
        inventory=json.dumps(json.loads(player[5]) if player[5] else []),
        minefield=json.dumps({
            "display": display_field,
            "real": real_field,
            "start_time": time.time()
        }),
        daily_quest=player[7],
        last_quest_date=player[8],
        title=player[9],
        frame=player[10],
        donate_currency=player[11]
    )

    await message.answer(
        f"⛏ Шахта готова к работе! Уровень: {player[4]}\nВыбери клетку для копания:",
        reply_markup=create_keyboard(display_field, real_field)
    )

@router.callback_query(F.data.startswith("mine_"))
async def process_mine_callback(callback: CallbackQuery):
    user_id = str(callback.from_user.id)
    player = await get_player(user_id)
    
    if not player:
        await callback.answer("⚠️ Сначала используй /start.")
        return

    # Парсим данные из callback
    _, row, col, cell_type = callback.data.split("_")
    row, col = int(row), int(col)
    
    resources = player[2]
    mine_level = player[4]
    fields = json.loads(player[6])
    display_field = fields["display"]
    real_field = fields["real"]
    start_time = fields.get("start_time", time.time())
    
    # Проверяем, не нажата ли уже открытая клетка
    if display_field[row][col] != HIDDEN:
        await callback.answer("Эта клетка уже открыта!")
        return

    # Обработка разных типов клеток
    if cell_type == ORE:
        resources += 1
        text = "⛏ Ты нашёл 1 руду!"
    elif cell_type == DIAMOND:
        resources += 5
        text = "💎 Ты нашёл алмаз! +5 руды!"
    elif cell_type == LOOT_BOX:
        resources += 3
        text = "🎁 Ты открыл лут-бокс! +3 руды!"
    elif cell_type == CAVE_IN:
        resources = max(0, resources - 2)
        text = "💥 Обвал! Ты потерял 2 руды!"
    else:
        text = "⬜ Пустая клетка."

    # Обновляем отображаемое поле
    display_field[row][col] = cell_type
    
    # Проверяем, все ли клетки открыты
    if is_field_completed(display_field):
        # Вычисляем время прохождения уровня
        time_spent = time.time() - start_time
        mine_level += 1
        
        # Определяем комбо-множитель
        combo_level = 0
        for level, time_limit in COMBO_TIMES.items():
            if time_spent <= time_limit:
                combo_level = level
            else:
                break
        
        # Вычисляем бонус с учетом комбо
        base_bonus = mine_level * 2
        combo_multiplier = COMBO_MULTIPLIERS.get(combo_level, 1.0)
        total_bonus = int(base_bonus * combo_multiplier)
        resources += total_bonus
        
        # Формируем текст с информацией о комбо
        text += f"\n\n🎉 Поздравляем! Ты завершил уровень {mine_level-1}!\n"
        if combo_level > 0:
            text += f"⚡️ Комбо x{combo_level}! Время: {int(time_spent)}с\n"
            text += f"🎁 Бонус за завершение: +{total_bonus} руды (базовый {base_bonus} x{combo_multiplier})\n"
        else:
            text += f"⏱ Время: {int(time_spent)}с\n"
            text += f"🎁 Бонус за завершение: +{total_bonus} руды\n"
        text += f"📈 Новый уровень шахты: {mine_level}"
        
        # Генерируем новое поле для следующего уровня
        display_field, real_field = generate_field(mine_level)
        start_time = time.time()
    
    # Сохраняем изменения
    await save_player(
        user_id=user_id,
        username=player[1],
        resources=resources,
        level=player[3],
        mine_level=mine_level,
        inventory=json.dumps(json.loads(player[5]) if player[5] else []),
        minefield=json.dumps({
            "display": display_field,
            "real": real_field,
            "start_time": start_time
        }),
        daily_quest=player[7],
        last_quest_date=player[8],
        title=player[9],
        frame=player[10],
        donate_currency=player[11]
    )

    # Обновляем сообщение с новым полем
    await callback.message.edit_text(
        f"{text}\n\nТвои ресурсы: {resources}\nУровень шахты: {mine_level}\nВыбери следующую клетку:",
        reply_markup=create_keyboard(display_field, real_field)
    )
    await callback.answer()
