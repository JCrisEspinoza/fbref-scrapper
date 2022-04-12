from sqlalchemy import Column, Integer, String, Float, ForeignKey

from database import Base

valid_keys = [
    "id",
    "user_id",
    "season",
    "goals",
    "shots_total",
    "shots_on_target",
    "shots_on_target_pct",
    "shots_total_per90",
    "shots_on_target_per90",
    "goals_per_shot",
    "goals_per_shot_on_target",
    "average_shot_distance",
    "pens_made",
    "pens_att"
]


class ShootingStats(Base):
    __tablename__ = 'shooting_stats'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    season = Column(String)
    goals = Column(Integer)
    shots_total = Column(Integer)
    shots_on_target = Column(Integer)
    shots_on_target_pct = Column(String)
    shots_total_per90 = Column(Float)
    shots_on_target_per90 = Column(Float)
    goals_per_shot = Column(String)
    goals_per_shot_on_target = Column(String)
    average_shot_distance = Column(String)
    pens_made = Column(Integer)
    pens_att = Column(Integer)

    def __init__(self, *args, **kwargs):
        new_kwargs = {pair[0]: pair[1] for pair in
                      filter(lambda pair: pair[0] in valid_keys and pair[1] not in ['', None], kwargs.items())}
        super(ShootingStats, self).__init__(*args, **new_kwargs)

    def __repr__(self):
        return f'ShootingStats({self.user_id})'

    def __str__(self):
        return f'{self.id} ({self.user_id})'
