import tkinter as tk
from tkinter import messagebox

n = 8
white_value = 1
black_value = -1

class OthelloGame:
    def __init__(self, root, black_player, white_player):
        self.root = root
        self.root.title("Othello Game")
        self.board = [[0]*n for _ in range(n)]
        self.board[3][3] = self.board[4][4] = white_value # White pieces
        self.board[3][4] = self.board[4][3] = black_value  # Black pieces
        self.current_player = black_value  # Black starts
        self.directions = [(-1,-1), (-1,0), (-1,1),
                          (0,-1),         (0,1),
                          (1,-1),  (1,0), (1,1)]
        self.buttons = [[None for _ in range(n)] for _ in range(n)]
        self.black_player = black_player
        self.white_player = white_player
        self.create_board()
        self.next_turn()

    def create_board(self):
        for x in range(n):
            for y in range(n):
                button = tk.Button(self.root, text="", width=4, height=2,
                                   command=lambda x=x, y=y: self.on_button_click(x, y))
                button.grid(row=x, column=y)
                self.buttons[x][y] = button
        self.update_board()

    def update_board(self):
        for x in range(n):
            for y in range(n):
                if self.board[x][y] == black_value:
                    self.buttons[x][y].config(text="", bg="black", fg="white")
                elif self.board[x][y] == white_value:
                    self.buttons[x][y].config(text="", bg="white", fg="black")
                else:
                    self.buttons[x][y].config(text="", bg="green")
        self.root.update()


    # used?
    def is_valid_position(self, x, y):
        return 0 <= x < n and 0 <= y < n
    
    # used? 
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

    # used? 
    def get_valid_moves(self, player):
        moves = []
        for x in range(n):
            for y in range(n):
                if self.is_valid_move(x, y, player):
                    moves.append((x, y))
        return moves

    # used? 
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

    # used? 
    def get_score(self):
        black = sum(row.count(-1) for row in self.board)
        white = sum(row.count(1) for row in self.board)
        return black, white

    # used? 
    def on_button_click(self, x, y):
        # if self.current_player == -1 and isinstance(self.black_player, HumanPlayer):
        if isinstance(self.black_player, HumanPlayer):
            if self.is_valid_move(x, y, self.current_player):
                self.make_move(x, y, self.current_player)
                self.update_board()
                self.current_player = -self.current_player
                self.root.after(500, self.next_turn)  # Delay for next move

    def next_turn(self):
        if self.current_player == black_value:
            player = self.black_player
        else:
            player = self.white_player

        if isinstance(player, ComputerPlayer):
            move = player.get_move(self.board, self.current_player)
            if move:
                self.make_move(move[0], move[1], self.current_player)
                self.update_board()
            self.current_player = -self.current_player
            self.root.after(500, self.next_turn)  # Delay for next move
        elif isinstance(player, HumanPlayer):
            # Wait for human input (handled in on_button_click)
            pass

        # Check if game is over
        if not self.get_valid_moves(-1) and not self.get_valid_moves(1):
            black, white = self.get_score()
            winner = "Black" if black > white else "White" if white > black else "Tie"
            messagebox.showinfo("Game Over", f"Final Score: Black {black} - White {white}\n{winner} wins!")
            self.root.quit()
        

class Player:
    def get_move(self, board, player):
        raise NotImplementedError

class HumanPlayer(Player):
    def get_move(self, board, player):
        # Human moves are handled by button clicks
        return None

class ComputerPlayer(Player):
    def get_move(self, board, player):
        # Greedy algorithm: choose move with most flips
        valid_moves = []
        for x in range(n):
            for y in range(n):
                if self.is_valid_move(board, x, y, player):
                    valid_moves.append((x, y))
        
        if not valid_moves:
            return None

        best_move = None
        max_flips = -1
        
        for (x, y) in valid_moves:
            temp_board = [row[:] for row in board]
            temp_board[x][y] = player
            flips = 0
            
            for dx, dy in [(-1,-1), (-1,0), (-1,1),
                          (0,-1),         (0,1),
                          (1,-1),  (1,0), (1,1)]:
                nx, ny = x + dx, y + dy
                temp_flips = 0
                while 0 <= nx < n and 0 <= ny < n and temp_board[nx][ny] == -player:
                    nx += dx
                    ny += dy
                    temp_flips += 1
                    
                if 0 <= nx < n and 0 <= ny < n and temp_board[nx][ny] == player:
                    flips += temp_flips
                    
            if flips > max_flips:
                max_flips = flips
                best_move = (x, y)
        
        return best_move

    def is_valid_move(self, board, x, y, player):
        if board[x][y] != 0:
            return False
        
        opponent = -player
        valid = False
        
        for dx, dy in [(-1,-1), (-1,0), (-1,1),
                      (0,-1),         (0,1),
                      (1,-1),  (1,0), (1,1)]:
            nx, ny = x + dx, y + dy
            temp_flips = 0
            while 0 <= nx < n and 0 <= ny < n and board[nx][ny] == opponent:
                nx += dx
                ny += dy
                temp_flips += 1
                
            if temp_flips > 0 and 0 <= nx < n and 0 <= ny < n and board[nx][ny] == player:
                valid = True
                
        return valid

# Choose players by commenting/uncommenting these lines
black_player = HumanPlayer()  # Human plays as Black
#black_player = ComputerPlayer()  # Computer plays as Black

#white_player = ComputerPlayer()  # Computer plays as White
white_player = HumanPlayer()  # Human plays as White

if __name__ == "__main__":
    root = tk.Tk()
    game = OthelloGame(root, black_player, white_player)
    root.mainloop()