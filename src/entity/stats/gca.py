from sqlalchemy import Column, Integer, String, Float, ForeignKey

from database import Base

valid_keys = [
    "id",
    "user_id",
    "season",
    "sca",
    "sca_per90",
    "sca_passes_live",
    "sca_passes_dead",
    "sca_dribbles",
    "sca_shots",
    "sca_fouled",
    "sca_defense",
    "gca",
    "gca_per90",
    "gca_passes_live",
    "gca_passes_dead",
    "gca_dribbles",
    "gca_shots",
    "gca_fouled",
    "gca_defense"
]


class GCAStats(Base):
    __tablename__ = 'gca_stats'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    season = Column(Integer)
    sca = Column(Integer)
    sca_per90 = Column(Float)
    sca_passes_live = Column(Integer)
    sca_passes_dead = Column(Integer)
    sca_dribbles = Column(Integer)
    sca_shots = Column(Integer)
    sca_fouled = Column(Integer)
    sca_defense = Column(Integer)
    gca = Column(Integer)
    gca_per90 = Column(Float)
    gca_passes_live = Column(Integer)
    gca_passes_dead = Column(Integer)
    gca_dribbles = Column(Integer)
    gca_shots = Column(Integer)
    gca_fouled = Column(Integer)
    gca_defense = Column(Integer)

    def __init__(self, *args, **kwargs):
        new_kwargs = {pair[0]: pair[1] for pair in
                      filter(lambda pair: pair[0] in valid_keys and pair[1] not in ['', None], kwargs.items())}
        super(GCAStats, self).__init__(*args, **new_kwargs)

    def __repr__(self):
        return f'{self.__tablename__}({self.user_id})'

    def __str__(self):
        return f'{self.id} ({self.user_id})'
