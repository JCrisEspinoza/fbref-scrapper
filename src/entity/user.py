from sqlalchemy import Column, Integer, String, Date, Float, Boolean
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = 'user'
    active = Column(Boolean, default=True)
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    external_id = Column(String, nullable=True, unique=True)
    country = Column(String, nullable=False)
    birth_date = Column(Date)
    birth_place = Column(String)
    url = Column(String)
    height = Column(Float)
    weight = Column(Float)
    position = Column(String)
    image = Column(String)
    misc_stats = relationship("MiscStats")
    basic_stats = relationship("BasicStats")
    shooting_stats = relationship("ShootingStats")
    time_stats = relationship("TimeStats")

    def __repr__(self):
        return f'Player({self.nombre})'

    def __str__(self):
        return self.nombre
