from enum import Enum
from collections import namedtuple

Direction = namedtuple('Direction', ('short_name', 'weights', 'oposite'))


class Directions(Enum):
    North = Direction('N', (0, -1), 'S')
    South = Direction('S', (0, 1), 'N')
    West = Direction('W', (-1, 0), 'E')
    East = Direction('E', (1, 0), 'W')


class RowStatus:
    Empty = 0
    Head = 1
    Body = 2
    Egg = 3
