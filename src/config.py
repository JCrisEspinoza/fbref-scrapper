from os import environ

SQL_ALCHEMY_ENGINE = environ.get('SQL_ALCHEMY_ENGINE', 'sqlite:///local.db.sqlite3')
