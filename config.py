from pathlib import Path
from fake_useragent import UserAgent

URL = "https://www.ozon.ru"
SHOP_URL = "https://www.ozon.ru/seller/gurman-ceremony/"
TIMEOUT = 1.5

def get_user_agent():
    ua = UserAgent(browsers=['chrome'], os=['windows'])
    return ua.random

USER_AGENT = get_user_agent()

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

LOG_FILE = DATA_DIR / "parser.log"
EXCEL_FILE = DATA_DIR / "gurman_ceremony.xlsx"
DB_FILE = DATA_DIR / "gurman_ceremony.db"

BRAVE_PROFILE_DIR = BASE_DIR / "brave_profile"
CDP_PORT = 9222