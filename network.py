import os
import shutil
import time
from pathlib import Path
from config import BRAVE_PROFILE_DIR, STATE_FILE, URL
from loguru import logger
from playwright.sync_api import sync_playwright

def kill_and_clean_locks():
    """Завершает ВСЕ процессы Brave и удаляет Singleton-файлы."""
    os.system("pkill -9 -f brave || true")
    time.sleep(1)

    lock_files = [
        Path(BRAVE_PROFILE_DIR) / "SingletonLock",
        Path(BRAVE_PROFILE_DIR) / "SingletonSocket",
        Path(BRAVE_PROFILE_DIR) / "SingletonCookie",
    ]
    for lock in lock_files:
        if lock.exists():
            try:
                lock.unlink()
            except Exception as e:
                logger.warning(f"Не удалось удалить {lock}: {e}")