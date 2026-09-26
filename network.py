import os
import shutil
import time
from pathlib import Path
from config import BRAVE_PROFILE_DIR, SHOP_URL, TIMEOUT
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

def check_browser() -> str | None:
    """Ищет бинарник Brave в системе."""
    browser_path = (
        shutil.which("brave-browser")
        or shutil.which("brave")
        or shutil.which("brave.exe")
    )
    if browser_path:
        logger.info(f"Найден браузер Brave: {browser_path}")
        return browser_path

    logger.error("Браузер Brave не найден в PATH!")
    return None

def fetch_all_pages() -> list[dict]:
    """Слушает сеть, собирает json ответы и скроллит страницу"""
    json_responses = []

    browser_path = check_browser()
    if not browser_path:
        logger.error("Нам нужен именно Brave")
        return []

    kill_and_clean_locks()

    with sync_playwright() as pw:
        try:
            logger.info("Запуск persistent-контекста Brave для сбора данных...")
            
            context = pw.chromium.launch_persistent_context(
                user_data_dir=BRAVE_PROFILE_DIR,
                executable_path=browser_path,
                headless=False,
                viewport=None,
                args=[
                    "--no-first-run",
                    "--no-default-browser-check",
                    "--disable-blink-features=AutomationControlled",
                    "--disable-extensions",
                    "--start-maximized",
                ],
                ignore_default_args=["--enable-automation"],
            )
        
            page = context.pages[0] if context.pages else context.new_page()
            
            def handle_response(response):
                """Обработчик сетевых ответов"""
                if (
                    "/api/entrypoint-api.bx/page/json/v2" in response.url
                    and response.status == 200
                ):
                    try:
                        json_data = response.json()
                        json_responses.append(json_data)
                        logger.info(f"Перехвачен пакет API {len(json_responses)}")
                    except Exception:
                        pass

            page.on("response", handle_response)

            logger.info("Открываем страницу магазина...")
            page.goto(SHOP_URL, timeout=45000, wait_until="domcontentloaded")
            page.wait_for_timeout(TIMEOUT * 1000)

            logger.info("Начинаем подгрузку всех товаров скроллингом...")
            while True:
                previous_height = page.evaluate("document.body.scrollHeight")
                page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                page.wait_for_timeout(int(TIMEOUT * 1000))
                new_height = page.evaluate("document.body.scrollHeight")
                if new_height == previous_height:
                    logger.info("Достигнут конец страницы, скролл завершен")
                    break

            logger.info(f"Сбор завершен. Всего успешно перехвачено ответов: {len(json_responses)}")

            context.close()

        except Exception as e:
            logger.error(f"Ошибка при сборе заказов: {e}")
        finally:
            kill_and_clean_locks()

    return json_responses