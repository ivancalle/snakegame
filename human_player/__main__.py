from pygame import Rect
from game.game import Game

from .player import Player

game = Game(False, 0, Rect(0, 0, 900, 900), 30, initial_speed=8)
game.load_game()
game_map = game.get_game_status()
player = Player()
while game.is_playable():
    game.check_events()
    direction = player.next_direction()
    game.play_turn(direction)

print(f"final score {game.score} in {game.turn} turns")
game.close()
