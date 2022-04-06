from sqlalchemy import Column, Integer, String, Date

from database import Base


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    external_id = Column(String, nullable=False)
    born_date = Column(Date, nullable=False)
    country = Column(String, nullable=False)
    info_page = Column(String, nullable=False)

    def __repr__(self):
        return f'Player({self.nombre})'

    def __str__(self):
        return self.nombre
