import random
import numpy as np

class EvalMiniMax:
    def __init__(self, player, max_depth = 3):
        self.player = player  # Player value (e.g., 1 for white, -1 for black)
        self.max_depth = max_depth
        self.piece_scores_4x4 = np.array([[1, 1, 1, 1],
                                        [1, 1, 1, 1],
                                        [1, 1, 1, 1],
                                        [1, 1, 1, 1]])
        self.piece_scores = np.block([[self.piece_scores_4x4, self.piece_scores_4x4],
                                    [self.piece_scores_4x4, self.piece_scores_4x4]])

    def move(self, env):
        validMoves = env.get_valid_moves(self.player)
        if validMoves == []:
            env.passed()
            return
        
        board = env.get_board()
        best_score = -np.inf
        best_move = None
        player = self.player

        for move in validMoves:
            score = self.minimax_search(env.update_board(board, move, player), 1, player, env)
            if score > best_score:
                best_score = score
                best_move = move
        env.make_move(best_move, self.player)


    def minimax_search(self, board, depth, player, env):
        if env.is_game_over(): return env.who_Won()*np.inf
        elif depth == self.max_depth: return np.sum(player * board * self.piece_scores)
        player = -player

        if env.get_possible_moves(board, player) == []:
            player = -player
            if env.get_possible_moves(board, player) == []:
                return np.sum(player * board * self.piece_scores)
        
        scores = [self.minimax_search(env.update_board(board, move, player), depth+1, player, env) for move in env.get_possible_moves(board, player)]
        scores = [player*score for score in scores]
        return max(scores)


    #def minimax_search(self, board, depth, player, env):
    #    if env.is_game_over(): return env.who_Won()*np.inf
    #    elif depth == self.max_depth: return np.sum(player * board * self.piece_scores)
    #    player = -player
    #    scores = [self.minimax_search(env.update_board(board, move, player), depth+1, player, env) for move in env.get_possible_moves(board, player)]
    #    scores = [player*score for score in scores]
    #    return max(scores)
    