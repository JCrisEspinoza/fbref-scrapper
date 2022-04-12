from sqlalchemy import Column, Integer, String, Float, ForeignKey

from database import Base

valid_keys = [
    "id",
    "user_id",
    "season",
    "passes_completed",
    "passes",
    "passes_pct",
    "passes_total_distance",
    "passes_progressive_distance",
    "passes_completed_short",
    "passes_short",
    "passes_pct_short",
    "passes_completed_medium",
    "passes_medium",
    "passes_pct_medium",
    "passes_completed_long",
    "passes_long",
    "passes_pct_long",
    "assists",
    "xa",
    "xa_net",
    "assisted_shots",
    "passes_into_final_third",
    "passes_into_penalty_area",
    "crosses_into_penalty_area",
    "progressive_passes"
]


class PassingStats(Base):
    __tablename__ = 'passing_stats'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    season = Column(Integer)
    passes_completed = Column(Integer)
    passes = Column(Integer)
    passes_pct = Column(Float)
    passes_total_distance = Column(Integer)
    passes_progressive_distance = Column(Integer)
    passes_completed_short = Column(Integer)
    passes_short = Column(Integer)
    passes_pct_short = Column(Float)
    passes_completed_medium = Column(Integer)
    passes_medium = Column(Integer)
    passes_pct_medium = Column(Float)
    passes_completed_long = Column(Integer)
    passes_long = Column(Integer)
    passes_pct_long = Column(Float)
    assists = Column(Integer)
    xa = Column(Float)
    xa_net = Column(Float)
    assisted_shots = Column(Integer)
    passes_into_final_third = Column(Integer)
    passes_into_penalty_area = Column(Integer)
    crosses_into_penalty_area = Column(Integer)
    progressive_passes = Column(Integer)

    def __init__(self, *args, **kwargs):
        new_kwargs = {pair[0]: pair[1] for pair in
                      filter(lambda pair: pair[0] in valid_keys and pair[1] not in ['', None], kwargs.items())}
        super(PassingStats, self).__init__(*args, **new_kwargs)

    def __repr__(self):
        return f'{self.__tablename__}({self.user_id})'

    def __str__(self):
        return f'{self.id} ({self.user_id})'
