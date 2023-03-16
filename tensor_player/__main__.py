import random
import gc
from time import time
from concurrent.futures import ThreadPoolExecutor

from pygame import Rect
from game.enums import Directions
from game.game import Game
from game.no_interface_game import NoInterfaceGame

from .player import Player
from .model import Model


generate_initial_population = False
training = False

if generate_initial_population:
    for i in range(100):
        Model().save(f'tensor_models/initial_population/{i}.json')
elif training:
    seed = random.randint(0, 999999999)
    print(f'SEED: {seed}')
    rating = []
    game = NoInterfaceGame(30)
    for i in range(100):
        before = time()
        player = Player(Model(f'tensor_models/initial_population/{i}.json'))
        game.load_game(seed)

        while game.is_playable() and game.turn < 100:
            direction = player.next_direction(game.get_game_status())
            game.play_turn(direction)

        print((i, game.score/game.turn), time()-before)
        rating.append((i, game.score/game.turn))
        del player._model

    print(sorted(rating, key=lambda x: x[1]))
else:
    player = Player(Model())
    game = Game(False, 0, Rect(0, 0, 900, 900), 30)
    game.load_game()

    while game.is_playable() and game.turn < 1000:
        game.check_events()
        direction = player.next_direction(game.get_game_status())
        game.play_turn(direction)

    print(f"final score {game.score} in {game.turn} turns")
    game.close()
