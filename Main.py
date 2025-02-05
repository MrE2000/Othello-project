import time
import tkinter as tk
from sys import argv

from Graphics import Graphics
from Othello import Othello
from players import *

# not global?
n = 8
white_value = 1
black_value = -1

def main():

    n_games = 1

    if len(argv) >= 1:
        try:
            n_games = int(argv[1])
        except: pass

    graphics = Graphics()
    env = Othello()

    n_wins = {
        1: 0,
        0: 0,
        -1: 0
    }

    count_draws = True

    #black_player = HumanPlayer(black_value, graphics)  # type: ignore # Human plays as Black
    black_player = RandomPlayer(black_value)
    # black_player = ComputerPlayer(black_value)  # Computer plays as Black

    #white_player = ComputerPlayer(white_value)  # Computer plays as White
    #white_player = HumanPlayer(white_value, graphics)  # type: ignore # Human plays as White
    white_player = RandomPlayer(white_value)

    n_played = 0
    while n_played < n_games:
        env.reset()
        graphics.draw(env.board)
        while True:
            black_player.move(env)
            graphics.draw(env.board)
            if env.is_game_over(): break

            white_player.move(env)
            graphics.draw(env.board)
            if env.is_game_over(): break

            if env.is_stalemate(): break

            # this doesnt work think its because humanplayer isnt seen
#        if isinstance(black_player, HumanPlayer) or isinstance(white_player, HumanPlayer):
#            time.sleep(1)
        
        winner = env.who_Won()
        n_wins[winner] += 1
        if count_draws:
            n_played += 1
        elif winner != 0:
            n_played += 1
            
        
        # stop graphics
    
    print('Results:')
    print(f'black_player won {100.0 * n_wins[1] / n_played}%')
    print(f'white_player won {100.0 * n_wins[-1] / n_played}%')
    print(f'draw             {100.0 * n_wins[0] / n_played}%')


if __name__ == "__main__": main()