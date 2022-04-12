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
    "passes",
    "passes_live",
    "passes_dead",
    "passes_free_kicks",
    "through_balls",
    "passes_pressure",
    "passes_switches",
    "crosses",
    "corner_kicks",
    "corner_kicks_in",
    "corner_kicks_out",
    "corner_kicks_straight",
    "passes_ground",
    "passes_low",
    "passes_high",
    "passes_left_foot",
    "passes_right_foot",
    "passes_head",
    "throw_ins",
    "passes_other_body",
    "passes_completed",
    "passes_offsides",
    "passes_oob",
    "passes_intercepted",
    "passes_blocked"
]


class PassingTypesStats(Base):
    __tablename__ = 'passing_types_stats'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    season = Column(Integer)
    age = Column(Integer)
    squad = Column(String)
    country = Column(String)
    comp_level = Column(String)
    lg_finish = Column(String)
    minutes_90s = Column(Float)
    passes = Column(Integer)
    passes_live = Column(Integer)
    passes_dead = Column(Integer)
    passes_free_kicks = Column(Integer)
    through_balls = Column(Integer)
    passes_pressure = Column(Integer)
    passes_switches = Column(Integer)
    crosses = Column(Integer)
    corner_kicks = Column(Integer)
    corner_kicks_in = Column(Integer)
    corner_kicks_out = Column(Integer)
    corner_kicks_straight = Column(Integer)
    passes_ground = Column(Integer)
    passes_low = Column(Integer)
    passes_high = Column(Integer)
    passes_left_foot = Column(Integer)
    passes_right_foot = Column(Integer)
    passes_head = Column(Integer)
    throw_ins = Column(Integer)
    passes_other_body = Column(Integer)
    passes_completed = Column(Integer)
    passes_offsides = Column(Integer)
    passes_oob = Column(Integer)
    passes_intercepted = Column(Integer)
    passes_blocked = Column(Integer)

    def __init__(self, *args, **kwargs):
        new_kwargs = {pair[0]: pair[1] for pair in
                      filter(lambda pair: pair[0] in valid_keys and pair[1] not in ['', None], kwargs.items())}
        super(PassingTypesStats, self).__init__(*args, **new_kwargs)

    def __repr__(self):
        return f'{self.__tablename__}({self.user_id})'

    def __str__(self):
        return f'{self.id} ({self.user_id})'
