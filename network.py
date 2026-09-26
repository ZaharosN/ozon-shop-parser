import os
import shutil
import time
from pathlib import Path
from config import BRAVE_PROFILE_DIR, STATE_FILE, URL
from loguru import logger
from playwright.sync_api import sync_playwright