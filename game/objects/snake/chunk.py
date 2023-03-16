from typing import Tuple

from pygame.sprite import Sprite
from pygame import Surface, transform


class SnakeChunk(Sprite):
    """Representing the snake player."""

    @classmethod
    def config(cls, image: Surface, containers: list, max_square_size: int):
        cls._image = transform.scale(image, (max_square_size-6, max_square_size-6))
        cls._containers = containers
        cls._max_square_size = max_square_size

    def __init__(self, position: Tuple[int, int]):
        super().__init__(self._containers)
        self.image = self._image
        self.rect = self.image.get_rect(topleft=(0, 0))
        self.move(position)

    def move(self, position: Tuple[int, int]):
        self.rect.center = position
