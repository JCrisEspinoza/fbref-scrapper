from database import Base, engine
from entity.user import User
from entity.stats import Stats

def sync():
    Base.metadata.create_all(engine)
