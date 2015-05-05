import os
import sys
PARENT_PATH = os.getcwd()[:-2]
sys.path.append(PARENT_PATH+'strategy')
import human
import iterative_deepening_strategy
import mcts_base
import mcts_arrange
import game_manager
import board

# flg constant for getStrategy(flg, me) method
MINI_MAX = 1
FLAT_MCTS = 2
TUNED_MCTS = 3

def getStrategy(flg, me):
    if flg == MINI_MAX:
        return iterative_deepening_strategy.IterativeDeepening(me)
    elif flg == FLAT_MCTS:
        return mcts_base.BaseMCTS(me)
    elif flg == TUNED_MCTS:
        return mcts_arrange.TunedMCTS(me)

# Initialize Objects
mGameManager = game_manager.GameManager()
mBoard = board.Board(4, 7, 6)
mBoard.setPlayer('O', 'X')

# show Menu and get Game information
mFirstStrategy, mSecondStrategy = 0, 0

if mGameManager.askPlayerIsCPU('FIRST PLAYER'):
    flg_strategy = mGameManager.askCPUStrategy()
    mFirstStrategy = getStrategy(flg_strategy, 'O')
    mGameManager.askStrategyParameter(flg_strategy, mFirstStrategy)
else:
    mFirstStrategy = human.Human('O')

if mGameManager.askPlayerIsCPU('SECOND PLAYER'):
    flg_strategy = mGameManager.askCPUStrategy()
    mSecondStrategy = getStrategy(flg_strategy, 'X')
    mGameManager.askStrategyParameter(flg_strategy, mSecondStrategy)
else:
    mSecondStrategy = human.Human('X')

#################################################################################
# If you want to read board state from in.txt file, change if_read_board to True.
if_read_board = False
mFirstStrategy.D = False
mSecondStrategy.D = False
#################################################################################
if_switch_player = False
if if_read_board:
    print 'Readed Board state !!';print ''
    if_switch_player = mGameManager.readBoard(mBoard)
    if if_switch_player:
        temp = mFirstStrategy
        mFirstStrategy = mSecondStrategy
        mSecondStrategy = temp

# Start Connect Four !!
mBoard.display()
print '> START THE GAME !!'

while True:

    if mBoard.checkIfDraw():
        print '> DRAW !!'
        break

    col = mFirstStrategy.think(mBoard)
    if col == -1:
        print '> FINISH THE GAME'
        break
    if_win = mBoard.update(mFirstStrategy.ME, col)
    mBoard.display()
    if if_win:
        if not if_switch_player: print '> FIRST PLAYER WIN !!'
        else: print '> SECOND PLAYER WIN !!'
        break
    
    col = mSecondStrategy.think(mBoard)
    if col == -1:
        print '> FINISH THE GAME'
        break
    if_win = mBoard.update(mSecondStrategy.ME, col)
    mBoard.display()
    if if_win:
        if not if_switch_player: print '> SECOND PLAYER WIN !!'
        else: print '> FIRST PLAYER WIN !!'
        break

print ''
