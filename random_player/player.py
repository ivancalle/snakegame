import random

from game.enums import RowStatus, Directions


class Player:
    def __init__(self):
        self._last_direction = None

    def next_direction(self) -> Directions | None:
        return random.choice([
            Directions.North,
            Directions.South,
            Directions.West,
            Directions.East
        ])
