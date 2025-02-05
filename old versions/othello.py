import tkinter as tk
from tkinter import messagebox

class OthelloGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Othello Game")
        self.n = 8
        self.board = [[0]*self.n for _ in range(self.n)]
        self.board[3][3] = self.board[4][4] = 1  # White pieces
        self.board[3][4] = self.board[4][3] = -1  # Black pieces
        self.current_player = -1  # Black starts
        self.directions = [(-1,-1), (-1,0), (-1,1),
                          (0,-1),         (0,1),
                          (1,-1),  (1,0), (1,1)]
        self.buttons = [[None for _ in range(self.n)] for _ in range(self.n)]
        self.create_board()

    def create_board(self):
        for x in range(self.n):
            for y in range(self.n):
                button = tk.Button(self.root, text="", width=4, height=2,
                                   command=lambda x=x, y=y: self.on_button_click(x, y))
                button.grid(row=x, column=y)
                self.buttons[x][y] = button
        self.update_board()

    def update_board(self):
        for x in range(self.n):
            for y in range(self.n):
                if self.board[x][y] == -1:
                    self.buttons[x][y].config(text="", bg="black", fg="white")
                elif self.board[x][y] == 1:
                    self.buttons[x][y].config(text="", bg="white", fg="black")
                else:
                    self.buttons[x][y].config(text="", bg="green")
        self.root.update()

    def is_valid_position(self, x, y):
        return 0 <= x < self.n and 0 <= y < self.n

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

    def get_valid_moves(self, player):
        moves = []
        for x in range(self.n):
            for y in range(self.n):
                if self.is_valid_move(x, y, player):
                    moves.append((x, y))
        return moves

    def make_move(self, x, y, player):
        if not self.is_valid_move(x, y, player):
            return False
        
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
                    
        return True

    def computer_move(self, player):
        valid_moves = self.get_valid_moves(player)
        if not valid_moves:
            return False

        # Greedy algorithm: choose move with most flips
        best_move = None
        max_flips = -1
        
        for (x, y) in valid_moves:
            temp_board = [row[:] for row in self.board]
            temp_board[x][y] = player
            flips = 0
            
            for dx, dy in self.directions:
                nx, ny = x + dx, y + dy
                temp_flips = 0
                while self.is_valid_position(nx, ny) and temp_board[nx][ny] == -player:
                    nx += dx
                    ny += dy
                    temp_flips += 1
                    
                if self.is_valid_position(nx, ny) and temp_board[nx][ny] == player:
                    flips += temp_flips
                    
            if flips > max_flips:
                max_flips = flips
                best_move = (x, y)
        
        if best_move:
            self.make_move(best_move[0], best_move[1], player)
            print(f"Computer plays at {best_move[0]}, {best_move[1]}")
            return True
        return False

    def get_score(self):
        black = sum(row.count(-1) for row in self.board)
        white = sum(row.count(1) for row in self.board)
        return black, white

    def on_button_click(self, x, y):
        if self.current_player == -1:  # Human player (Black)
            if self.is_valid_move(x, y, self.current_player):
                self.make_move(x, y, self.current_player)
                self.update_board()
                self.current_player = -self.current_player
                self.root.after(500, self.computer_turn)  # Delay for computer move
            else:
                messagebox.showinfo("Invalid Move", "Invalid move! Try again.")

    def computer_turn(self):
        if self.current_player == 1:  # Computer player (White)
            if self.computer_move(self.current_player):
                self.update_board()
                self.current_player = -self.current_player
            else:
                self.current_player = -self.current_player

        # Check if game is over
        if not self.get_valid_moves(-1) and not self.get_valid_moves(1):
            black, white = self.get_score()
            winner = "Black" if black > white else "White" if white > black else "Tie"
            messagebox.showinfo("Game Over", f"Final Score: Black {black} - White {white}\n{winner} wins!")
            self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    game = OthelloGame(root)
    root.mainloop()