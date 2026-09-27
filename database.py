import sqlite3
from loguru import logger
from config import DB_FILE

def get_connection():
    """Создает подключение к базе данных SQL"""
    return sqlite3.connect(DB_FILE)

def init_db():
    """Сохдает таблицу в БД если её не существует"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS gurman_cremony (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sku TEXT UNIQUE NOT NULL,
            title TEXT,
            price REAL,
            old_price REAL,
            discount REAL,
            rating TEXT,
            reviews TEXT,
            link TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.commit()
    logger.info(f"База данных инициализирована: {DB_FILE}")    