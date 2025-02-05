import numpy as np

# not global?
n = 8
white_value = 1
black_value = -1
class Othello:
    def __init__(self):
        self.board = np.zeros((n, n), dtype=int)
        self.directions = [(-1,-1), (-1,0), (-1,1),
                           (0,-1),          (0,1),
                           (1,-1),  (1,0) , (1,1)]
        self.n_passed = 0

    def get_board(self): # should be used by algorithms
        return self.board.copy()

    def reset(self):
        self.board[:,:] = 0
        self.board[3][3] = self.board[4][4] = white_value
        self.board[3][4] = self.board[4][3] = black_value
        self.winner = 0

    def is_game_over(self):
        return not np.any(self.board == 0)
    
    def get_valid_moves(self, player):
        moves = []
        for x in range(n):
            for y in range(n):
                if self.is_valid_move(x, y, player):
                    moves.append((x, y))
        return moves

    def is_valid_move(self, x, y, player):
        if self.board[x][y] != 0:
            return False
        
        opponent = -player
        valid = False
        
        for dx, dy in self.directions:
            nx, ny = x + dx, y + dy
            temp_flips = 0
            while self.is_valid_position(nx, ny) and self.board[nx][ny] == opponent:
                nx += dx
                ny += dy
                temp_flips += 1
                
            if temp_flips > 0 and self.is_valid_position(nx, ny) and self.board[nx][ny] == player:
                valid = True
                
        return valid

    def is_valid_position(self, x, y):
        return 0 <= x < n and 0 <= y < n
    
    def make_move(self, move, player):
        x = move[0]        
        y = move[1]    

        self.board[x][y] = player
        opponent = -player
        
        for dx, dy in self.directions:
            nx, ny = x + dx, y + dy
            to_flip = []
            while self.is_valid_position(nx, ny) and self.board[nx][ny] == opponent:
                to_flip.append((nx, ny))
                nx += dx
                ny += dy
                
            if self.is_valid_position(nx, ny) and self.board[nx][ny] == player:
                for (fx, fy) in to_flip:
                    self.board[fx][fy] = player
    
    def who_Won(self):
        sum = np.sum(self.board)
        if sum > 0:
            return 1
        elif sum < 0:
            return -1
        return 0
    
    def passed(self):
        self.n_passed += 1

    def is_stalemate(self):
        if self.n_passed == 2:
            return True
        self.n_passed = 0
        return False