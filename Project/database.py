import aiosqlite

DB_NAME = "players.db"

async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS players (
                user_id TEXT PRIMARY KEY,
                username TEXT,
                resources INTEGER DEFAULT 0,
                level INTEGER DEFAULT 1,
                mine_level INTEGER DEFAULT 1,
                inventory TEXT,
                minefield TEXT,
                daily_quest TEXT,
                last_quest_date TEXT,
                title TEXT DEFAULT '',
                frame TEXT DEFAULT '',
                donate_currency INTEGER DEFAULT 0
            )
        ''')
        await db.commit()

async def get_player(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("SELECT * FROM players WHERE user_id = ?", (user_id,))
        row = await cursor.fetchone()
        return row

async def save_player(user_id, username, resources, level, mine_level,
                      inventory, minefield, daily_quest="", last_quest_date="",
                      title="", frame="", donate_currency=0):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''
            INSERT INTO players (
                user_id, username, resources, level, mine_level,
                inventory, minefield, daily_quest, last_quest_date,
                title, frame, donate_currency
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
                username=excluded.username,
                resources=excluded.resources,
                level=excluded.level,
                mine_level=excluded.mine_level,
                inventory=excluded.inventory,
                minefield=excluded.minefield,
                daily_quest=excluded.daily_quest,
                last_quest_date=excluded.last_quest_date,
                title=excluded.title,
                frame=excluded.frame,
                donate_currency=excluded.donate_currency
        ''', (
            user_id, username, resources, level, mine_level,
            inventory, minefield, daily_quest, last_quest_date,
            title, frame, donate_currency
        ))
        await db.commit()

async def get_top_players(limit=10):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute('''
            SELECT user_id, username, resources, level, mine_level, title, frame, donate_currency
            FROM players
            ORDER BY mine_level DESC, resources DESC
            LIMIT ?
        ''', (limit,))
        return await cursor.fetchall()
