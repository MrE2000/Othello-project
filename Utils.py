import numpy as np


n = 8

directions = [(-1,-1), (-1,0), (-1,1),
              (0,-1),          (0,1),
              (1,-1),  (1,0) , (1,1)]

def get_valid_moves(board, player):
        moves = []
        for x in range(n):
            for y in range(n):
                if is_valid_move(board, player, x, y):
                    moves.append((x, y))
        return moves

def is_valid_move(board, player, x, y):
        if board[x][y] != 0:
            return False
        
        opponent = -player
        valid = False
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            temp_flips = 0
            while is_valid_position(nx, ny) and board[nx][ny] == opponent:
                nx += dx
                ny += dy
                temp_flips += 1
                
            if temp_flips > 0 and is_valid_position(nx, ny) and board[nx][ny] == player:
                valid = True
                
        return valid


def is_valid_position(x, y):
    return 0 <= x < n and 0 <= y < n

def update_board(board, player, move): # should be used by algorithms
    board = board.copy()

    x = move[0]        
    y = move[1]    

    board[x][y] = player
    opponent = -player
    
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        to_flip = []
        while is_valid_position(nx, ny) and board[nx][ny] == opponent:
            to_flip.append((nx, ny))
            nx += dx
            ny += dy
            
        if is_valid_position(nx, ny) and board[nx][ny] == player:
            for (fx, fy) in to_flip:
                board[fx][fy] = player

    return board


def is_game_over(board):
    return get_valid_moves(board, 1) == [] and get_valid_moves(board, -1) == []

def who_won(board):
    sum = np.sum(board)
    if sum > 0:
        return 1
    elif sum < 0:
        return -1
    return 0