from database import Base, engine
from entity.user import User


def sync():
    Base.metadata.create_all(engine)
