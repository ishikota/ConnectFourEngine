from abs_strategy import BaseStrategy

class RandomStrategy(BaseStrategy):

    def __init__(self, me):
        super(RandomStrategy, self).__init__(me)

    # concrete method of thinking process.
    # just return all possible columns.
    def makeANextMove(self, board):
        best_moves = []
        for c,r in enumerate(board.position):
            if r != board.HEIGHT:
                best_moves.append(c)
        return best_moves
