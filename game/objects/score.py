import pygame


class Score(pygame.sprite.Sprite):
    """to keep track of the score."""

    def __init__(self, containers: list):
        pygame.sprite.Sprite.__init__(self, containers)
        self.font = pygame.font.Font(None, 20)
        self.font.set_italic(1)
        self.color = "white"
        self._score = 0
        self._to_update = True
        self.update()
        self.rect = self.image.get_rect().move(10, 450)

    @property
    def score(self) -> int:
        return self._score

    def add_score(self, amount: int = 1):
        self._score += amount
        self._to_update = True

    def update(self):
        """We only update the score in update() when it has changed."""
        if self._to_update:
            msg = "Score: %d" % self._score
            self.image = self.font.render(msg, 0, self.color)
            self.to_update = False
