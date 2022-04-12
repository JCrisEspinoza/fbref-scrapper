from sqlalchemy import Column, Integer, String, Float, ForeignKey

from database import Base

valid_keys = [
    "id",
    "user_id",
    "season",
    "season_start_date",
    "season_end_date",
    "age",
    "squad",
    "country",
    "comp_level",
    "lg_finish",
    "games",
    "games_starts",
    "minutes",
    "minutes_90s",
    "goals",
    "assists",
    "goals_pens",
    "pens_made",
    "pens_att",
    "cards_yellow",
    "cards_red",
    "goals_per90",
    "assists_per90",
    "goals_assists_per90",
    "goals_pens_per90",
    "goals_assists_pens_per90",
    "xg",
    "npxg",
    "xa",
    "npxg_xa",
    "xg_per90",
    "xa_per90",
    "xg_xa_per90",
    "npxg_per90",
    "npxg_xa_per90"
]


class BasicStats(Base):
    __tablename__ = 'basic_stats'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    season = Column(String)
    season_start_date = Column(Integer)
    season_end_date = Column(Integer)
    age = Column(Integer)
    squad = Column(String)
    country = Column(String)
    comp_level = Column(String)
    lg_finish = Column(String)
    games = Column(Integer)
    games_starts = Column(Integer)
    minutes = Column(Integer)
    minutes_90s = Column(Float)
    goals = Column(Integer)
    assists = Column(Integer)
    goals_pens = Column(Integer)
    pens_made = Column(Integer)
    pens_att = Column(Integer)
    cards_yellow = Column(Integer)
    cards_red = Column(Integer)
    goals_per90 = Column(Float)
    assists_per90 = Column(Float)
    goals_assists_per90 = Column(Float)
    goals_pens_per90 = Column(Float)
    goals_assists_pens_per90 = Column(Float)
    xg = Column(Float)
    npxg = Column(Float)
    xa = Column(Float)
    npxg_xa = Column(Float)
    xg_per90 = Column(Float)
    xa_per90 = Column(Float)
    xg_xa_per90 = Column(Float)
    npxg_per90 = Column(Float)
    npxg_xa_per90 = Column(Float)

    def __init__(self, *args, **kwargs):
        new_kwargs = {pair[0]: pair[1] for pair in
                      filter(lambda pair: pair[0] in valid_keys and pair[1] not in ['', None], kwargs.items())}

        dates = new_kwargs.get("season").split("-")

        new_kwargs["season_start_date"] = int(dates[0])
        new_kwargs["season_end_date"] = int(dates[-1])

        super(BasicStats, self).__init__(*args, **new_kwargs)

    def __repr__(self):
        return f'BasicStats({self.user_id})'

    def __str__(self):
        return f'{self.id} ({self.user_id})'
