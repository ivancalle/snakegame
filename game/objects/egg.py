from random import Random

from pygame.sprite import Sprite
from pygame import Surface, Rect, transform


class Egg(Sprite):
    """Representing the snake player."""

    @classmethod
    def config(cls, image: Surface, containers: list, max_square_size: int, screen_rect: Rect, seed: int | None = None):
        cls._image = transform.scale(image, (max_square_size, max_square_size))
        cls._containers = containers
        cls._max_square_size = max_square_size
        cls._screen_rect = screen_rect
        cls._random = Random(seed)

    def __init__(self):
        super().__init__(self._containers)
        self.image = self._image
        self.rect = self.image.get_rect(topleft=(0, 0))
        self._y_posibilities = list(range(0, self._screen_rect.height, self._max_square_size))
        self._x_posibilities = list(range(0, self._screen_rect.width, self._max_square_size))
        self.move([(0, 0)])

    def set_random_position(self):
        self.rect.left = self._random.choice(self._x_posibilities)
        self.rect.top = self._random.choice(self._y_posibilities)

    def move(self, baned_positions: list):
        self.set_random_position()

        while self.rect.center in baned_positions:
            self.set_random_position()
