# Ozon Shop Parser

Парсер витрины продавца на Ozon с экспортом в SQLite и Excel.
Работает через перехват внутренних API-запросов, обходит антибот-защиту 
с помощью Brave Browser.


Сбор каталога магазина [Gurman Ceremony](https://www.ozon.ru/seller/gurman-ceremony/) 
— китайский чай и сопутствующие товары. Собрано 134 товара.

## Что собираем

- Название товара
- Цена (числом, для сортировки)
- Старая цена и скидка
- Рейтинг
- Количество отзывов
- Ссылка на карточку

## Стек

- **Python 3.12+**
- **Playwright** + **Brave Browser** (обход антибот-защиты Ozon)
- **SQLite** (хранение с дедубликацией по SKU)
- **openpyxl** (экспорт в Excel с форматированием)
- **loguru** (логирование)

## Архитектура

├── config.py # Настройки: URL, пути, константы
├── auth.py # Утилиты: поиск браузера, очистка locks
├── network.py # Сбор JSON-пакетов через перехват API
├── parser.py # Парсинг товаров из BDUI-структуры
├── database.py # Сохранение в SQLite
├── saver.py # Экспорт в Excel с форматированием
├── main.py # Оркестратор
└── data/ # Результаты (.db, .xlsx)


## Установка

```bash
git clone <repo>
cd ozon-shop-parser
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium
```


## Важно: нужен установленный Brave Browser. На Linux:
sudo apt install brave-browser

## Запуск
python main.py


Скрипт откроет Brave, прокрутит витрину продавца, соберёт все товары
и сохранит результаты в data/