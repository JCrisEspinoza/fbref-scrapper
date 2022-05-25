from database import Base, engine
from entity.user import User
import entity.stats

def sync():
    Base.metadata.create_all(engine)
