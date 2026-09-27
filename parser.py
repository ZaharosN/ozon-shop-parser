import json
from loguru import logger

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
                all_products.extend(item)

    logger.info(f"Всего уникальных товаров: {len(all_products)}")
    return all_products