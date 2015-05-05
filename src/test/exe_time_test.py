import os
import sys

PARENT_PATH = os.getcwd()[:-4]
sys.path.append(PARENT_PATH+'ui')
sys.path.append(PARENT_PATH+'strategy')

import time
import board
import iterative_deepening_strategy
import mcts_base
import mcts_arrange

def setParameter(i, param, s):
    if i==0: # MiniMax(IterativeDeepening)
        s.setParameter(s.DEPTH_LIMIT_MODE, param)
    elif i==1: # Flat MCTS
        s.setParameter(s.RANDOM_PLAYOUT, param, 0, False)
    elif i==2: # Arranged MCTS
        s.setParameter(s.MODE_PLAYOUT_NUM_LIMIT, param, 1)

b = board.Board(4,7,6)
b.setPlayer('O', 'X')

strategy =[]
strategy.append(iterative_deepening_strategy.IterativeDeepening(b.USER))
strategy.append(mcts_base.BaseMCTS(b.USER))
strategy.append(mcts_arrange.TunedMCTS(b.USER))

divider = ''
for i in range(50): divider += '='

print divider
print ''
print '**** EXECUTION TIME TEST ****'
print ''

size = len(strategy)
for i in range(size):
    s = strategy[i]
    print ''
    print 'Strategy : '+s.__class__.__name__
    print ''
    param = 0
    while True: # search depth loop
        diff = 1 if i==0 else 100 # i==0 => IterativeDeepening else => MCTS
        param += diff
        setParameter(i, param, s)
        start_time = time.time()
        s.makeANextMove(b)
        end_time = time.time()
        exe_time = end_time - start_time

        text = 'Search Depth is '+str(param) if i==0 else 'Number of Playout is '+str(param)
        print text+' : ['+str(exe_time)+'(s)]'
        if exe_time>5: break
    print divider

print ''
print 'FINISHED'
print ''
