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
            CREATE TABLE IF NOT EXISTS gurman_ceremony (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sku TEXT UNIQUE NOT NULL,
            title TEXT,
            price INTEGER,
            old_price INTEGER,
            discount TEXT,
            rating REAL,
            reviews INTEGER,
            link TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.commit()
    logger.info(f"База данных инициализирована: {DB_FILE}")  
  

def save_to_db(products: list[dict]) -> int:
    """Сохраняет список товаров а БД, возвращает кол-во добавленных записей"""
    if not products:
        logger.warning("Нет данных для сохранения в БД")
        return 0
      
    init_db()
    added_count = 0
    with get_connection() as conn:
        cursor = conn.cursor()
        for item in products:
            try:
                cursor.execute(
                    """
                    INSERT OR IGNORE INTO gurman_ceremony (sku, title, price, old_price, discount, rating, reviews, link)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        item.get("sku"),
                        item.get("title"),
                        item.get("price"),
                        item.get("old_price"),
                        item.get("discount"),
                        item.get("rating"),
                        item.get("reviews"),
                        item.get("link")
                    ),
                )
                if cursor.rowcount > 0:
                    added_count += 1
            except Exception as e:
                logger.error(f"Ошибка записи SKU {item.get('sku')} в БД: {e}")

        conn.commit()
    logger.success(f"Успешно добавлено новых записей в БД: {added_count} (из {len(products)})")
    return added_count  