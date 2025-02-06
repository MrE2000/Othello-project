import random

from Utils import *

class RandomPlayer:
    def __init__(self, player):
        self.player = player  # Player value (e.g., 1 for white, -1 for black)

    def move(self, env):
        validMoves = get_valid_moves(env.board, self.player)
        if validMoves == []:
            return
        
        move = random.choice(validMoves)
        
        env.make_move(move, self.player)