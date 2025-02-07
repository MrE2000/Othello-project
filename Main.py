import time
import tkinter as tk
import numpy as np
from sys import argv

from Graphics import Graphics
from Othello import Othello
from players import *
from Utils import *

# not global?
n = 8
white_value = 1
black_value = -1

def main():

    n_games = 1

    if len(argv) >= 1:  # TODO add arg for playing as white or black against the AI for the executable
                        # TODO add arg for time limit selection for AI search
        try:
            n_games = int(argv[1])
        except: pass

    graphics = Graphics()
    env = Othello()

    n_wins = {
        white_value: 0,
        0: 0,
        black_value: 0
    }


    # TODO use time limit for figure out max depth of AI player
    #black_player = HumanPlayer(black_value, graphics)  # type: ignore # Human plays as Black
    black_player = RandomPlayer(black_value)
    # black_player = ComputerPlayer(black_value)  # Computer plays as Black
    #black_player = EvalMiniMax(black_value, 3)


    #white_player = ComputerPlayer(white_value)  # Computer plays as White
    #white_player = HumanPlayer(white_value, graphics)  # type: ignore # Human plays as White
    white_player = EvalMiniMax(white_value, 3)

    n_played = 0
    
    start_time = time.time()
    while n_played < n_games:
        env.reset()
        graphics.draw(env.board)
        while True:
            black_player.move(env)
            graphics.draw(env.board)
            if is_game_over(env.board): break

            white_player.move(env)
            graphics.draw(env.board)
            if is_game_over(env.board): break

            # this doesnt work think its because humanplayer isnt seen
#        if isinstance(black_player, HumanPlayer) or isinstance(white_player, HumanPlayer):
#            time.sleep(1)
        
        winner = who_won(env.board)
        print(np.sum(env.board))
        n_wins[winner] += 1
        n_played += 1
    
    elapsed_time = time.time() - start_time
    graphics.root.quit()

        # stop graphics 
    
    print('Results:')
    print(f'black_player won {100.0 * n_wins[black_value] / n_played}%')
    print(f'white_player won {100.0 * n_wins[white_value] / n_played}%')
    print(f'draw             {100.0 * n_wins[0] / n_played}%')
    print()
    print(f"Total elapsed time: {elapsed_time:.6f} seconds")
    print(f"Average elapsed time: {elapsed_time/n_played:.6f} seconds")


if __name__ == "__main__": main()