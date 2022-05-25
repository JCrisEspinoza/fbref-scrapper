from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import config

engine = create_engine(config.SQL_ALCHEMY_ENGINE)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


