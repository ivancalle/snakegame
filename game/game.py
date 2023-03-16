import os
from queue import Queue

import pygame
import numpy

from .objects.snake import SnakeChunk, SnakeHead
from .objects.egg import Egg
from .objects.score import Score
from .enums import Directions, RowStatus

main_dir = os.path.split(os.path.abspath(__file__))[0]


class Game:
    @staticmethod
    def _load_image(file):
        """loads an image, prepares it for play"""
        file = os.path.join(main_dir, "resources", "images", file)
        try:
            surface = pygame.image.load(file)
        except pygame.error:
            raise SystemExit('Could not load image "%s" %s' % (file, pygame.get_error()))
        return surface.convert()

    def __init__(
        self,
        fullscreen: bool,
        winstyle: int,
        screen_rect: pygame.Rect,
        square_size: int,
        initial_speed: int = 0
    ):
        # Initialize pygame
        self._turn = 1
        self._initial_speed = initial_speed
        self._quit_pressed = False
        if pygame.get_sdl_version()[0] == 2:
            pygame.mixer.pre_init(44100, 32, 2, 1024)
        pygame.init()
        if pygame.mixer and not pygame.mixer.get_init():
            print("Warning, no sound")
            pygame.mixer = None

        self._screen_rect = screen_rect
        self._square_size = square_size

        if screen_rect.height % self._square_size != 0 or screen_rect.width % self._square_size != 0:
            raise SystemExit('Invalid square_size')

        self._fullscreen = fullscreen
        # Set the display mode
        self._winstyle = winstyle  # |FULLSCREEN
        self._bestdepth = pygame.display.mode_ok(screen_rect.size, self._winstyle, 32)
        self._screen = pygame.display.set_mode(screen_rect.size, self._winstyle, self._bestdepth)

    def load_game(self, seed=None):
        self._clock = pygame.time.Clock()

        head_img = pygame.Surface((100, 100))
        head_img.fill((0, 0, 255))

        egg_img = self._load_image('bomb.gif')

        body_img = pygame.Surface((100, 100))
        body_img.fill((0, 255, 0))

        self._body_group = pygame.sprite.Group()
        self._egg_group = pygame.sprite.GroupSingle()
        self._all_group = pygame.sprite.RenderUpdates()

        SnakeHead.config(head_img, [self._all_group], self._square_size, self._screen_rect)
        Egg.config(egg_img, [self._all_group, self._egg_group], self._square_size, self._screen_rect, seed)
        SnakeChunk.config(body_img, [self._all_group, self._body_group], self._square_size)

        bgdtile = pygame.Surface((self._square_size-2, self._square_size-2))
        bgdtile.fill((255, 255, 255))
        self._background = pygame.Surface(self._screen_rect.size)
        for y in range(0, self._screen_rect.height, self._square_size):
            for x in range(0, self._screen_rect.width, self._square_size):
                self._background.blit(bgdtile, (x+1, y+1))
        self._screen.blit(self._background, (0, 0))
        pygame.display.flip()

        self._head = SnakeHead()
        self._egg = Egg()
        self._score = Score([self._all_group])

        self._body = Queue()

    def is_playable(self):
        return not self._quit_pressed and self._head.alive()

    def _set_value_on_coords(self, game_map: list, rect: pygame.Rect, value: int):
        coords = rect.topleft
        game_map[coords[1]//self._square_size][coords[0]//self._square_size] = value

    def get_game_status(self):
        game_map = numpy.zeros((self._screen_rect.width // self._square_size,
                               self._screen_rect.height // self._square_size))
        # game_map = [[RowStatus.Empty for _ in range(0, self._screen_rect.width // self._square_size)]
        #             for _ in range(0, self._screen_rect.height // self._square_size)]

        self._set_value_on_coords(game_map, self._head.rect, RowStatus.Head)
        self._set_value_on_coords(game_map, self._egg.rect, RowStatus.Egg)
        new_body = Queue()
        while not self._body.empty():
            chunk = self._body.get()
            self._set_value_on_coords(game_map, chunk.rect, RowStatus.Body)
            new_body.put(chunk)

        self._body = new_body

        return game_map

    @property
    def score(self) -> int:
        return self._score.score

    @property
    def turn(self) -> int:
        return self._turn

    def play_turn(self, direction: Directions):
        # Run our main loop whilst the player is alive.
        if self.is_playable():
            self._turn += 1

            # clear/erase the last drawn sprites
            self._all_group.clear(self._screen, self._background)

            # update all the sprites
            self._all_group.update()

            last_head_position = self._head.rect.center
            self._head.move(direction)

            if pygame.sprite.spritecollide(self._head, self._egg_group, 0):
                self._egg.move([last_head_position, self._egg.rect.center])
                self._score.add_score()
                self._body.put(SnakeChunk(last_head_position))
            elif not self._body.empty():
                last_chunk = self._body.get()
                last_chunk.move(last_head_position)
                self._body.put(last_chunk)

            if pygame.sprite.spritecollide(self._head, self._body_group, 0):
                self._head.kill()

            # draw the scene
            dirty = self._all_group.draw(self._screen)
            pygame.display.update(dirty)

            self._clock.tick(self._initial_speed)

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._quit_pressed = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self._quit_pressed = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    if not self._fullscreen:
                        print("Changing to FULLSCREEN")
                        self._screen_backup = self._screen.copy()
                        self._screen = pygame.display.set_mode(
                            self._screen_rect.size, self._winstyle | pygame.FULLSCREEN, self._bestdepth
                        )
                        self._screen.blit(self._screen_backup, (0, 0))
                    else:
                        print("Changing to windowed mode")
                        self._screen_backup = self._screen.copy()
                        self._screen = pygame.display.set_mode(
                            self._screen_rect.size, self._winstyle, self._bestdepth
                        )
                        self._screen.blit(self._screen_backup, (0, 0))
                    pygame.display.flip()
                    self._fullscreen = not self._fullscreen

    def close(self):
        if pygame.mixer:
            pygame.mixer.music.fadeout(1000)
        pygame.time.wait(1000)
