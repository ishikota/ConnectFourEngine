'''
this script competes two strategy for specified times and display game result.
** Work Flow **
First, The kinds of strategy to compete is asked when you execute this script.
Second, the number of times to play game is asked.
Finally, this script starts to compete specified two strategy, and display result.
** parameter format **
[flg_first_strategy, first_strategy_mode, first_strategy_param, first_use_heuristic,
 flg_second_strategy, second_strategy_mode, second_strategy_param]
 @param flg_***_strategy : 1 => MiniMax(IteraticeDeepening), 2 => Flat MCTS 3 => Arranged MCTS
 @param ***_strategy_mode : 1 => depth/playout_num limit, 2 => time limit
 @param ***_strategy_param : the number of parameter (like search_depth, time limit(s))
 @param ***_use_heuristic : 1 => use heuristic , 2 => do not use heurstic
 
 ** parameter example **
 [1,2,3,1,3,2,3,2,10]
 => Execute below match for 10 times
    MiniMax(IterativeDeepening) : thinking limit is 3(s) and use heuristic.
            VS
    TunedMCTS : thinking limit is 3(s) (and not use heuristic)

'''
import os
import sys

PARENT_PATH = os.getcwd()[:-4]
sys.path.append(PARENT_PATH+'ui')
sys.path.append(PARENT_PATH+'strategy')

import iterative_deepening_strategy
import mcts_base
import mcts_arrange
import game_simulator
import game_manager
import time
import sys
from sys import stdout

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

def setParameter(s, flg, mode, param, use_heuristic):
    if flg == MINI_MAX:
        if mode == 1: s.setParameter(s.DEPTH_LIMIT_MODE, param)
        else: s.setParameter(s.TIME_LIMIT_MODE, param)
        s.USE_HEURISTIC = use_heuristic
    elif flg == FLAT_MCTS:
        if mode == 1: s.setParameter(s.RANDOM_PLAYOUT, param, 0, false)
        else: s.setParameter(s.RANDOM_PLAYOUT, param, 0, false)
    elif flg == TUNED_MCTS:
        if mode == 1: s.setParameter(s.MODE_PLAYOUT_NUM_LIMIT, param, 8)
        else: s.setParameter(s.MODE_TIME_LIMIT, param, 8)

simulator = game_simulator.GameSimulator()
simulator.d = False
gm = game_manager.GameManager()

# read parameter
p = sys.argv[1]
p = p.split(',')
for i in range(len(p)):
    p[i] = int(p[i])
s1 = getStrategy(p[0], 'O')
setParameter(s1, p[0],p[1],p[2],p[3])
s2 = getStrategy(p[4], 'X')
setParameter(s2, p[4],p[5],p[6],p[7])
N = int(p[8])
result = [0 for i in range(3)]
for i in range(N):
    stdout.flush()
    stdout.write('\r The %d/%d th Game now...' % (i+1, N))
    result = simulator.play(s1, s2)
    results[result] += 1
    if result == 0: print 'DRAW'
    elif result == 1: print 'WIN'
    else: print 'LOSE'
stdout.write('\n')

# display result
s1_name = s1.__class__.__name__
s2_name = s2.__class__.__name__
print ''
print s1_name +' VS '+s2_name
print s1_name+'  win against '+s2_name+' : '+str(results[1])
print s1_name+' lose against '+s2_name+' : '+str(results[2])
print s1_name+' draw against '+s2_name+' : '+str(results[0])
print ''
ft = time.time()

print ''
print 'EXECUTION TIME : '+str(int(ft-st))+'(s)'
print ''
