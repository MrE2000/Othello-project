class HumanPlayer:
    def __init__(self, player, graphics):
        self.player = player  # Player value (e.g., 1 for white, -1 for black)
        self.graphics = graphics

    def move(self, env):
        validMoves = env.get_valid_moves(self.player)
        if validMoves == []: 
            env.passed()
            return
        noMoveMade = True
        move = None
        while noMoveMade:
            if self.graphics.requested_move == None:
                pass
            else:
                (x, y) = self.graphics.requested_move
                self.graphics.requested_move = None
                if (x, y) in validMoves:
                    env.board[x, y] = self.player
                    noMoveMade = False
                    move = (x, y)
            self.graphics.root.update()
            
            
        
        env.make_move(move, self.player)
