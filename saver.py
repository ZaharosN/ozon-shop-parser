from loguru import logger
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from config import EXCEL_FILE

def save_to_excel(products: list[dict], filename: str = EXCEL_FILE) -> str:
    """Сохраняет список товаров в отформатированный файл Excel"""
    if not products:
        logger.error("Нет данных для сохранения в Excel")
        return ""

    wb = Workbook()
    ws = wb.active
    ws.title = "Чаи"

    headers = ["SKU", "Название", "Цена (руб.)", "Старая цена", "Скидка", "Рейтинг", "Отзывы", "Ссылка"]
    ws.append(headers)

    head_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    head_fill = PatternFill(start_color="4F81BD", end_color="4F81BD", fill_type="solid")
    head_alig = Alignment(horizontal="center", vertical="center")

    for cell in ws[1]:
        cell.font = head_font
        cell.fill = head_fill
        cell.alignment = head_alig

    for item in products:
        row = [
            item.get("sku"),
            item.get("title"),
            item.get("price"),
            item.get("old_price"),
            item.get("discount"),
            item.get("rating"),
            item.get("reviews"),
            item.get("link")
        ]
        ws.append(row)

    for col in ws.columns:
        max_len = 0
        col_letter = col[0].column_letter
        for cell in col:
            if cell.value:
                max_len = max(max_len, len(str(cell.value)))

        ws.column_dimensions[col_letter].width = max(max_len + 3, 12)

    wb.save(filename)
    logger.success(f"Данные успешно сохранены в Excel: {filename} (Всего строк: {len(products)})")

    return filename