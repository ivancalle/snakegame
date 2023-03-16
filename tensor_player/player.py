from game.enums import Directions

from .model import Model


class Player:
    def __init__(self, model: Model):
        self._last_direction = None
        self._model = model

    def next_direction(self, game_map: list) -> Directions | None:
        return self._model.predict(game_map)
