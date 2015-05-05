import abc
import heuristic
import random
import warnings

class BaseStrategy(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, me):
        # ME   is the piece of player who use this strategy.
        # OPPO is the piece of opponent (against ME.)
        # D is debug flag
        self.ME = me
        self.OPPO ='X' if me == 'O' else 'O' 
        self.Heuristic = heuristic.Heuristic(self.ME, self.OPPO)
        self.USE_HEURISTIC = True
        self.USE_STRONG_HEURISTIC = False
        self.D = False

    @abc.abstractmethod
    def makeANextMove(self, board):
        # This method is abstract method.
        # Return next move's row and column position. 
        # by following subclass's strategy.
        # Return -1, -1 , if cannot find good move.
        # then next move is chosen randomly.
        pass

    def randomChoice(self, board, best_moves):
        # This method is called when all of next move's score is same,
        # choice next move randomly.
        # (But do not choice the columns which already full-stacked.)
        for col in best_moves:
            if board.position[col] == board.HEIGHT:
                best_moves.remove(col)
        col = random.choice(best_moves)
        return col

    def setParameter(self):
        # This method is abstract method.
        # sub class implements this method to
        # adjut strategy parameter from main 
        # program.
        pass

    def setHeuristicParameter(self, w1,w2,w3,w4,w5,w6):
        self.Heuristic.setParameter(w1,w2,w3,w4,w5,w6)

    def think(self, board):
        # This method is called from main loop.
        # Subclass implements thinking process.
        best_moves = self.makeANextMove(board)

        # error handling for chaning type of return value

        if self.D: print 'BEST MOVES : '+str(best_moves)
        if self.USE_STRONG_HEURISTIC:
            best_moves = self.Heuristic.choiceByStrongHeuristic(board,best_moves)
        elif self.USE_HEURISTIC:
            best_moves = self.Heuristic.choiceByHeuristic(board, best_moves)
        if self.D: print 'BEST HEURISTIC MOVES : '+str(best_moves)
        col = self.randomChoice(board, best_moves)
        return col






    ### DEPRECATED!! ###
    # Some Error would occur when you use call this method. 
    # Use "think(board)" method instead.
    def thinkWithHeuristic(self, board):
        raise Exception, '"abs_strategy.thinkWithHeuristic(board)" method is deprecated. Use "abs_strategy.think(board)" method instead.'
        # First choice best moves by following subclass's strategy.
        # From the best moves, choice best one move by using heuristic value.
        best_moves = self.makeANextMove(board)
        col = self.Heuristic.choiceByHeuristic(board, best_moves)
        return col
