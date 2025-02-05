import random

class RandomPlayer:
    def __init__(self, player):
        self.player = player  # Player value (e.g., 1 for white, -1 for black)

    def move(self, env):
        validMoves = env.get_valid_moves(self.player)
        if validMoves == []:
            env.passed()
            return
        
        move = random.choice(validMoves)
        
        env.make_move(move, self.player)