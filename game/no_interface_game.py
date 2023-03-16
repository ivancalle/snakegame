import os
from random import Random

import numpy

from .enums import Directions, RowStatus

main_dir = os.path.split(os.path.abspath(__file__))[0]


class NoInterfaceGame:
    def __init__(self, board_size: int):
        self._turn = 1
        self._board_size = board_size
        self._game_status = None
        self._random = None
        self._is_playable = True
        self._last_direction = None

    def load_game(self, seed=None):
        self._random = Random(seed)
        self._is_playable = True
        self._turn = 1
        head_position = tuple([self._board_size//2-(0 if self._board_size % 2 else 1)]*2)

        self._score = 0
        self._game_status = {
            "head": head_position,
            "body": []
        }
        self._set_egg()

    def is_playable(self):
        return self._is_playable

    def get_game_status(self):
        game_map = numpy.zeros((self._board_size, self._board_size))

        game_map[self._game_status['egg'][1]][self._game_status['egg'][0]] = RowStatus.Egg
        game_map[self._game_status['head'][1]][self._game_status['head'][0]] = RowStatus.Head

        for chunk in self._game_status['body']:
            game_map[chunk[1]][chunk[0]] = RowStatus.Body

        return game_map

    @property
    def score(self) -> int:
        return self._score

    @property
    def turn(self) -> int:
        return self._turn

    def _set_egg(self):
        no_valid = [self._game_status['head'], *self._game_status['body']]
        egg = self._game_status['head']
        while egg in no_valid:
            x_pos = self._random.randint(0, self._board_size-1)
            y_pos = self._random.randint(0, self._board_size-1)
            egg = (x_pos, y_pos)
        self._game_status['egg'] = egg

    def play_turn(self, direction: Directions):
        # Run our main loop whilst the player is alive.
        if self.is_playable():
            self._turn += 1

            direction = direction or self._last_direction
            if direction is None:
                return

            next_position = ((self._game_status['head'][0]+direction.value.weights[0]) % self._board_size,
                             (self._game_status['head'][1]+direction.value.weights[1]) % self._board_size)

            if next_position in self._game_status['body']:
                self._is_playable = False
                return

            self._game_status['body'].append(self._game_status['head'])
            self._game_status['head'] = next_position
            if next_position == self._game_status['egg']:
                self._score += 1
                self._set_egg()
            else:
                del self._game_status['body'][0]
