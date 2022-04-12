from sqlalchemy import Column, Integer, String, Float, ForeignKey

from database import Base

valid_keys = [
    "id",
    "user_id",
    "season",
    "age",
    "squad",
    "country",
    "comp_level",
    "lg_finish",
    "minutes_90s",
    "tackles",
    "tackles_won",
    "tackles_def_3rd",
    "tackles_mid_3rd",
    "tackles_att_3rd",
    "dribble_tackles",
    "dribbles_vs",
    "dribble_tackles_pct",
    "dribbled_past",
    "pressures",
    "pressure_regains",
    "pressure_regain_pct",
    "pressures_def_3rd",
    "pressures_mid_3rd",
    "pressures_att_3rd",
    "blocks",
    "blocked_shots",
    "blocked_shots_saves",
    "blocked_passes",
    "interceptions",
    "tackles_interceptions",
    "clearances",
    "errors"
]


class DefenseStats(Base):
    __tablename__ = 'defense_stats'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    season = Column(Integer)
    age = Column(Integer)
    squad = Column(String)
    country = Column(String)
    comp_level = Column(String)
    lg_finish = Column(String)
    minutes_90s = Column(Float)
    tackles = Column(Integer)
    tackles_won = Column(Integer)
    tackles_def_3rd = Column(Integer)
    tackles_mid_3rd = Column(Integer)
    tackles_att_3rd = Column(Integer)
    dribble_tackles = Column(Integer)
    dribbles_vs = Column(Integer)
    dribble_tackles_pct = Column(Float)
    dribbled_past = Column(Integer)
    pressures = Column(Integer)
    pressure_regains = Column(Integer)
    pressure_regain_pct = Column(Float)
    pressures_def_3rd = Column(Integer)
    pressures_mid_3rd = Column(Integer)
    pressures_att_3rd = Column(Integer)
    blocks = Column(Integer)
    blocked_shots = Column(Integer)
    blocked_shots_saves = Column(Integer)
    blocked_passes = Column(Integer)
    interceptions = Column(Integer)
    tackles_interceptions = Column(Integer)
    clearances = Column(Integer)
    errors = Column(Integer)

    def __init__(self, *args, **kwargs):
        new_kwargs = {pair[0]: pair[1] for pair in
                      filter(lambda pair: pair[0] in valid_keys and pair[1] not in ['', None], kwargs.items())}
        super(DefenseStats, self).__init__(*args, **new_kwargs)

    def __repr__(self):
        return f'{self.__tablename__}({self.user_id})'

    def __str__(self):
        return f'{self.id} ({self.user_id})'
