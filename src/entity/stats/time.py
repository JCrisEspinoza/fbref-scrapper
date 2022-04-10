from sqlalchemy import Column, Integer, String, Float, ForeignKey

from database import Base

valid_keys = [
    "",
    "id",
    "user_id",
    "season",
    "age",
    "squad",
    "country",
    "comp_level",
    "lg_finish",
    "games",
    "minutes",
    "minutes_per_game",
    "minutes_pct",
    "minutes_90s",
    "games_starts",
    "minutes_per_start",
    "games_complete",
    "games_subs",
    "minutes_per_sub",
    "unused_subs",
    "points_per_match",
    "on_goals_for",
    "on_goals_against",
    "plus_minus",
    "plus_minus_per90",
    "plus_minus_wowy"
]


class TimeStats(Base):
    __tablename__ = 'time_stats'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    season = Column(String)
    age = Column(Integer)
    squad = Column(String)
    country = Column(String)
    comp_level = Column(String)
    lg_finish = Column(String)
    games = Column(Integer)
    minutes = Column(String)
    minutes_per_game = Column(Integer)
    minutes_pct = Column(Float)
    minutes_90s = Column(Float)
    games_starts = Column(Integer)
    minutes_per_start = Column(Integer)
    games_complete = Column(Integer)
    games_subs = Column(Integer)
    minutes_per_sub = Column(String)
    unused_subs = Column(Integer)
    points_per_match = Column(Float)
    on_goals_for = Column(Integer)
    on_goals_against = Column(Integer)
    plus_minus = Column(Integer)
    plus_minus_per90 = Column(Float)
    plus_minus_wowy = Column(Float)

    def __init__(self, *args, **kwargs):
        new_kwargs = {pair[0]: pair[1] for pair in
                      filter(lambda pair: pair[0] in valid_keys and pair[1] not in ['', None], kwargs.items())}
        super(TimeStats, self).__init__(*args, **new_kwargs)

    def __repr__(self):
        return f'TimeStats({self.user_id})'

    def __str__(self):
        return f'{self.id} ({self.user_id})'
