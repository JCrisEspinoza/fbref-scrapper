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
    "touches",
    "touches_def_pen_area",
    "touches_def_3rd",
    "touches_mid_3rd",
    "touches_att_3rd",
    "touches_att_pen_area",
    "touches_live_ball",
    "dribbles_completed",
    "dribbles",
    "dribbles_completed_pct",
    "players_dribbled_past",
    "nutmegs",
    "carries",
    "carry_distance",
    "carry_progressive_distance",
    "progressive_carries",
    "carries_into_final_third",
    "carries_into_penalty_area",
    "miscontrols",
    "dispossessed",
    "pass_targets",
    "passes_received",
    "passes_received_pct",
    "progressive_passes_received"
]


class PossessionStats(Base):
    __tablename__ = 'possession_stats'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    season = Column(Integer)
    age = Column(Integer)
    squad = Column(String)
    country = Column(String)
    comp_level = Column(String)
    lg_finish = Column(String)
    minutes_90s = Column(Float)
    touches = Column(Integer)
    touches_def_pen_area = Column(Integer)
    touches_def_3rd = Column(Integer)
    touches_mid_3rd = Column(Integer)
    touches_att_3rd = Column(Integer)
    touches_att_pen_area = Column(Integer)
    touches_live_ball = Column(Integer)
    dribbles_completed = Column(Integer)
    dribbles = Column(Integer)
    dribbles_completed_pct = Column(Float)
    players_dribbled_past = Column(Integer)
    nutmegs = Column(Integer)
    carries = Column(Integer)
    carry_distance = Column(Integer)
    carry_progressive_distance = Column(Integer)
    progressive_carries = Column(Integer)
    carries_into_final_third = Column(Integer)
    carries_into_penalty_area = Column(Integer)
    miscontrols = Column(Integer)
    dispossessed = Column(Integer)
    pass_targets = Column(Integer)
    passes_received = Column(Integer)
    passes_received_pct = Column(Float)
    progressive_passes_received = Column(Integer)

    def __init__(self, *args, **kwargs):
        new_kwargs = {pair[0]: pair[1] for pair in
                      filter(lambda pair: pair[0] in valid_keys and pair[1] not in ['', None], kwargs.items())}
        super(PossessionStats, self).__init__(*args, **new_kwargs)

    def __repr__(self):
        return f'{self.__tablename__}({self.user_id})'

    def __str__(self):
        return f'{self.id} ({self.user_id})'
