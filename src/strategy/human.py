import os
import sys
PARENT_PATH = os.getcwd()[:-8]
sys.path.append(PARENT_PATH+'ui')
import game_manager
from abs_strategy import BaseStrategy

class Human(BaseStrategy):

    def __init__(self, me):
        super(Human, self).__init__(me)
        self.USE_HEURISTIC = False
        self.gameManager = game_manager.GameManager()

    def makeANextMove(self, board):
        player_str = ('FIRST' if self.ME == 'O' else 'SECOND' )\
                + 'PLAYER ('+self.ME+')'
        col = self.gameManager.getInput(player_str, board)
        return col

    def think(self, board):
        return self.makeANextMove(board)

