import os
import sys

PARENT_PATH = os.getcwd()[:-4]
sys.path.append(PARENT_PATH+'ui')
sys.path.append(PARENT_PATH+'strategy')

import time
import board
import game_manager
import game_simulator

import minimax_strategy
import alpha_beta_cut_strategy
import iterative_deepening_strategy
import mcts_strategy

'''  ***  PARAMETER LIST  ***
strategy1 -> mBoard.USER, mBoard.CPU
strategy2 -> mBoard.CPU, mBoard.USER
IterativeDeepening
    iterative_deepening_strategy.IterativeDeepening()
    .setParameter(mode, limit)
        mode -> TIME_LIMIT_MODE , DEPTH_LIMIT_MODE
MCTS
    mcts_strategy.MCTS()
    .setParameter(playoutpolicy, playoutnum, searchdepth, useheuristic)
        policy -> RANDOM_PLAYOUT, FUTURE_READ_PLAYOUT
'''
# init
g = game_manager.GameManager()
b = board.Board(4,6,6)
b.setPlayer('O', 'X')
sim = game_simulator.GameSimulator()
p1 = mcts_strategy.MCTS(b.USER, b.CPU)
p1.setParameter(p1.FUTURE_READ_PLAYOUT, 120, 2, False)
#p1.D = True
p2 = iterative_deepening_strategy.IterativeDeepening(b.USER, b.CPU)
p2.setParameter(p2.DEPTH_LIMIT_MODE, 10)
#p2.D = True
# read board
g.readBoard(b)

#calculate answer
answer = [p2.thinkWithHeuristic(b)]

TEST_NUM = 10
counts = [0 for i in range(b.WIDTH)]
calc_t = 0
for i in range(TEST_NUM):
    st = time.time()
    col = p1.makeANextMove(b)
    ft = time.time()
    calc_t += ft-st
    print 'TEST '+str(i)+':'+str(col)
    counts[col[0]] += 1

# calcurate accuracy rate
accuracy_rate = 0
for col in answer:
    accuracy_rate += counts[col]
accuracy_rate = 1.0*accuracy_rate/TEST_NUM
calc_t = calc_t/TEST_NUM

# show result
policy = 'RANDOM PLAYOUT' if p1.PLAYOUT_POLICY==0 else 'FUTURE READ PLAYOUT'
h = ' with heuristic ' if p1.USE_HEURISTIC else ' without heuristic '
print ''
print '*** RESULT ***'
print ''
print 'MCTS'+h+'('+policy+', PLAYOUT='+str(p1.PLAYOUT_NUM)+', DEPTH='+str(p1.SEARCH_DEPTH)+')'
print 'Answer           : '+str(answer)
print 'Choice Result    : '+str(counts)
print 'Accuracy rate    : '+str(accuracy_rate*100)+'%'
print 'Average Exe Time : '+str(calc_t)
print ''
print '**************'
print ''
