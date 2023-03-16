from pygame import Rect
from game.game import Game

from .player import Player

game = Game(False, 0, Rect(0, 0, 900, 900), 30)
game.load_game()
player = Player()


while game.is_playable() and game.turn < 10000:
    game.check_events()
    direction = player.next_direction(game.get_game_status())
    game.play_turn(direction)

print(f"final score {game.score} in {game.turn} turns")
game.close()
