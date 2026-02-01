from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "journal.db"

THEME_SIM_THRESHOLD = 0.32
RECENT_ENTRY_COUNT = 7
WEEK_DAYS = 7
