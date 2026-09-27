from network import fetch_all_pages
from parser import parse_all_products
from database import save_to_db
from saver import save_to_excel
from loguru import logger

def main():
    """Главная функция"""
    try:
        json_responses = fetch_all_pages()
        if not json_responses:
            logger.warning("Не удалось получить данные")
            return
            
        products = parse_all_products(json_responses)
        if not products:
            logger.warning("Не удалось распарсить данные")
            return

        added_count = save_to_db(products)
        save_to_excel(products)
        logger.success(f"=== Работа завершена успешно! Добавлено товаров в БД: {added_count} ===")
    except KeyboardInterrupt:
        logger.warning("Прервано пользователем")
    except Exception as e:
        logger.error(f'Ошибка в главной функции: {e}')

if __name__ == "__main__":
    main()