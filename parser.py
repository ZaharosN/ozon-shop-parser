import json
import re
from loguru import logger
from urllib.parse import urljoin
from config import URL

def extract_products(json_responses: list[dict]) -> list[dict]:
    """Извлекает уникальные товары из всех JSON-пакетов"""
    seen_sku = set()
    all_products = []

    for pkg in json_responses:
        widget_states = pkg.get("widgetStates", {})
        for key, value in widget_states.items():
            if "tileGridDesktop" not in key:
                continue

            try:
                inner = json.loads(value)
            except(json.JSONDecodeError, TypeError):
                continue
            items = inner.get("items", [])

            for item in items:
                sku = item.get('sku') or item.get('id')
                if sku in seen_sku:
                    continue
                seen_sku.add(sku)
                all_products.append(item)

    logger.info(f"Всего уникальных товаров: {len(all_products)}")
    return all_products

def parse_product(item: dict) -> dict:
    """Парсит один товар"""
    product = {
        "sku": None,
        "title": None,
        "price": None,
        "old_price": None,
        "discount": None,
        "rating": None,
        "reviews": None,
        "link": None,
    }

    # SKU
    product["sku"] = item.get("sku") or item.get("id")

    # Ссылка
    try:
        link = item["action"]["link"]
        product["link"] = urljoin(URL, link)
    except (KeyError, TypeError):
        pass

    for block in item.get("mainState", []):
        block_type = block.get("type")

        # Название
        if block.get("id") == "name":
            try:
                product["title"] = block["textDS"]["text"]
            except (KeyError, TypeError):
                pass

        # Цена
        if block_type == "priceV2":
            try:
                prices = block["priceV2"]["price"]
                product["price"] = prices[0]["text"]
                if len(prices) > 1:
                    product["old_price"] = prices[1]["text"]
                product["discount"] = block["priceV2"].get("discount")
            except (KeyError, IndexError, TypeError):
                pass

        # Рейтинг и отзывы
        if block_type == "labelListV2":
            test_id = block.get("labelListV2", {}).get("testInfo", {}).get("automatizationId")
            if test_id == "tile-list-rating":
                try:
                    texts = [
                        i["text"]["text"]
                        for i in block["labelListV2"]["items"]
                        if i.get("type") == "text"
                    ]
                    if len(texts) >= 1:
                        product["rating"] = texts[0]
                    if len(texts) >= 2:
                        product["reviews"] = texts[1]
                except (KeyError, TypeError):
                    pass

    return product