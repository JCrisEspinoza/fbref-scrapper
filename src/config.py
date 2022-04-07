from os import environ
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.resolve().parent
SQL_ALCHEMY_ENGINE = environ.get('SQL_ALCHEMY_ENGINE', 'sqlite:///≤base_dir>/dist/local.db.sqlite3') \
    .replace("≤base_dir>", str(BASE_DIR))

FBREF_BASE_URL = 'https://fbref.com/'
FBREF_COUNTRIES_TO_SCRAP = environ.get('FBREF_COUNTRIES_TO_SCRAP', 'BRA/Brasil-Football-players').split(',')
