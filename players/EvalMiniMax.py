import random
import numpy as np

from Utils import *

class EvalMiniMax:
    def __init__(self, player, max_depth = 3):
        self.player = player  # Player value (e.g., 1 for white, -1 for black)
        self.max_depth = max_depth
        
        # "Value map" for different tiles to own; our own experimental version
        self.piece_scores_4x4 = np.array([
            [10, 3, 3, 3],
            [3, 1, 1, 1],
            [3, 1, 1, 1],
            [3, 1, 1, 1]
        ])
        # Construct remaining quadrants
        mirrored_horizontal = self.piece_scores_4x4[:, ::-1]  # upper right
        mirrored_vertical = self.piece_scores_4x4[::-1]       # lower left
        mirrored_both = mirrored_horizontal[::-1]             # lower right
        # Combine
        self.piece_scores = np.block([
            [self.piece_scores_4x4, mirrored_horizontal],
            [mirrored_vertical, mirrored_both]
        ])

    def move(self, env):
        validMoves = get_valid_moves(env.board, self.player)
        if validMoves == []:
            return
        
        board = env.get_board()
        best_score = -np.inf
        best_move = None
        player = self.player

        #
        score = 0
        #
        
        for move in validMoves:
            #score = self.negamax_pruning(update_board(board, player, move), 1, player, env, -np.inf, np.inf)
            score = self.negamax(update_board(board, player, move), 1, player, env)
            if score > best_score or score == best_score == -np.inf:
                best_score = score
                best_move = move

        env.make_move(best_move, self.player)

    
    # Variant of minimax that condenses it down to one function recursion, instead of two calling each other
    # We found negamax on wikipedia: https://en.wikipedia.org/wiki/Negamax
    def negamax_pruning(self, board, depth, player, env, alpha, beta):
        if is_game_over(board): return who_won(board) * player * np.inf
        if depth == self.max_depth: return np.sum(player * board * self.piece_scores)  # should replace with generic "heuristic_eval"
    
        score = -np.inf
        for move in get_valid_moves(board, -player):
            score = max(score, -self.negamax_pruning(update_board(board, -player, move),  depth+1, -player, env, -beta, -alpha))
            alpha = max(alpha, score)
            if (alpha >= beta):
                break
        return score
    
    #no alpha-beta
    def negamax(self, board, depth, player, env):
        if is_game_over(board): return who_won(board) * player * np.inf
        if depth == self.max_depth: return np.sum(player * board * self.piece_scores)  # should replace with "heuristic_eval" to make generic
            
        score = -np.inf
        for move in get_valid_moves(board, -player):
            score = max(score, -self.negamax(update_board(board, -player, move),  depth+1, -player, env))
        return score
