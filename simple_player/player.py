from game.enums import RowStatus, Directions


class Player:
    def __init__(self):
        self._last_direction = None

    def next_direction(self, game_map: list) -> Directions | None:
        head = None
        egg = None
        for i, value in enumerate(game_map):
            for j, row_status in enumerate(value):
                if row_status == RowStatus.Head:
                    head = (i, j)
                elif row_status == RowStatus.Egg:
                    egg = (i, j)
                elif head is not None and egg is not None:
                    break
            if head is not None and egg is not None:
                break

        if egg[0] < head[0]:
            return Directions.North
        elif egg[0] > head[0]:
            return Directions.South
        elif egg[1] < head[1]:
            return Directions.West
        elif egg[1] > head[1]:
            return Directions.East
