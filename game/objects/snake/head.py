from pygame.sprite import Sprite
from pygame import Surface, Rect, transform

from ...enums import Directions


class SnakeHead(Sprite):
    """Representing the snake player."""

    @classmethod
    def config(cls, image: Surface, containers: list, max_square_size: int, screen_rect: Rect):
        cls._image = transform.scale(image, (max_square_size-6, max_square_size-6))
        cls._containers = containers
        cls._max_square_size = max_square_size
        cls._screen_rect = screen_rect

    def __init__(self):
        super().__init__(self._containers)
        self.image = self._image
        center = self._screen_rect.center
        if (self._screen_rect.width//self._max_square_size) % 2 == 0:
            center = (center[0]-self._max_square_size/2, center[1])
        if (self._screen_rect.height//self._max_square_size) % 2 == 0:
            center = (center[0], center[1]-self._max_square_size/2)

        self.rect = self.image.get_rect(center=center)
        self._last_direction = None

    def move(self, direction: Directions):
        direction = direction or self._last_direction

        if direction:
            if self._last_direction and direction.value.short_name == self._last_direction.value.oposite:
                direction = self._last_direction

            self.rect.top = (
                self.rect.top + direction.value.weights[1] * self._max_square_size) % self._screen_rect.height
            self.rect.left = (
                self.rect.left + direction.value.weights[0] * self._max_square_size) % self._screen_rect.height

        self._last_direction = direction
