from sqlalchemy import Column, Integer, String, Float, ForeignKey

from database import Base

valid_keys = [
    "id",
    "user_id",
    "season",
    "cards_yellow",
    "cards_red",
    "cards_yellow_red",
    "fouls",
    "fouled",
    "offsides",
    "crosses",
    "interceptions",
    "tackles_won",
    "pens_won",
    "pens_conceded",
    "own_goals"
]


class MiscStats(Base):
    __tablename__ = 'misc_stats'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    season = Column(String)
    cards_yellow = Column(Integer)
    cards_red = Column(Integer)
    cards_yellow_red = Column(Integer)
    fouls = Column(Integer)
    fouled = Column(Integer)
    offsides = Column(Integer)
    crosses = Column(Integer)
    interceptions = Column(Integer)
    tackles_won = Column(Integer)
    pens_won = Column(String)
    pens_conceded = Column(String)
    own_goals = Column(Integer)

    def __init__(self, *args, **kwargs):
        new_kwargs = {pair[0]: pair[1] for pair in
                      filter(lambda pair: pair[0] in valid_keys and pair[1] not in ['', None], kwargs.items())}
        super(MiscStats, self).__init__(*args, **new_kwargs)

    def __repr__(self):
        return f'MiscStats({self.user_id})'

    def __str__(self):
        return f'{self.id} ({self.user_id})'
