import sqlite3
from loguru import logger
from config import DB_FILE

def get_connection():
    """Создает подключение к базе данных SQL"""
    return sqlite3.connect(DB_FILE)

    