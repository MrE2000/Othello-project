import tkinter as tk

import numpy as np ## are Canvas, N, W, E, S  used?


# not global?
n = 8
white_value = 1
black_value = -1

class Graphics:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Othello Game")
        self.setup_board()

        self.requested_move = None
        
    def setup_board(self): # not ideal that buttons are made even if only computors play
        self.buttons = [[None for _ in range(n)] for _ in range(n)]

        for x in range(n):
            for y in range(n):
                button = tk.Button(self.root, text="", width=4, height=2,
                                   command=lambda x=x, y=y: self.on_click(x, y))
                button.grid(row=x, column=y)
                self.buttons[x][y] = button

    def draw(self, board):
        for x in range(n):
            for y in range(n):
                if board[x][y] == black_value:
                    self.buttons[x][y].config(text="", bg="black", fg="white")
                elif board[x][y] == white_value:
                    self.buttons[x][y].config(text="", bg="white", fg="black")
                else:
                    self.buttons[x][y].config(text="", bg="green")
        self.root.update()

    def on_click(self, x, y):
        self.requested_move = (x,y)

    