from entity.stats.basic import BasicStats
from entity.stats.defense import DefenseStats
from entity.stats.gca import GCAStats
from entity.stats.passing import PassingStats
from entity.stats.passing_types import PassingTypesStats
from entity.stats.possesion import PossessionStats
from entity.stats.shooting import ShootingStats
from entity.stats.time import TimeStats
from entity.stats.misc import MiscStats

stats_relationships = {
    'basic': BasicStats,
    'misc': MiscStats,
    'time': TimeStats,
    'shooting': ShootingStats,
    'passing': PassingStats,
    'passing_types': PassingTypesStats,
    'gca': GCAStats,
    'defense': DefenseStats,
    'possession': PossessionStats
}
