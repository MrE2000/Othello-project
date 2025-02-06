from Utils import*

class Player:
    def move(self, env):
        raise NotImplementedError
    
    def exists_no_move(self, board):
        validMoves = get_valid_moves(board, self.player) # move this to a func in player and call it from all players
        if validMoves == []: 
            return True
        return False