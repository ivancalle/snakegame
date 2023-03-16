
import pygame
from game.enums import RowStatus, Directions


class Player:
    def next_direction(self):
        keystate = pygame.key.get_pressed()
        direction = None
        if keystate[pygame.K_UP]:
            direction = Directions.North
        elif keystate[pygame.K_DOWN]:
            direction = Directions.South
        elif keystate[pygame.K_RIGHT]:
            direction = Directions.East
        elif keystate[pygame.K_LEFT]:
            direction = Directions.West

        return direction
