import os
import sys

PARENT_PATH = os.getcwd()[:-4]
sys.path.append(PARENT_PATH+'ui')
sys.path.append(PARENT_PATH+'strategy')

import random_strategy
import iterative_deepening_strategy
import game_simulator
import time
st = time.time()

simulator = game_simulator.GameSimulator()
simulator.d = False

s2 =  random_strategy.RandomStrategy('X', 'O')
s2.USE_STRONG_HEURISTIC = True

for depth in range(1,9):
    print 'depth:'+str(depth)
    s1 =  iterative_deepening_strategy.IterativeDeepening('O', 'X')
    s1.setParameter(s1.DEPTH_LIMIT_MODE, depth)
    s1.USE_HEURISTIC = False
    p2 = 'RandomStrategy'
    p1 =  'MiniMax (MAX DEPTH = '+str(depth)+')'
    N = 1 # the number of game to play
    results = [0 for ii in range(3)]
    for i in range(N):
        #print 'The '+str(i+1)+'th Game now...'
        result = simulator.play(s1, s2)
        results[result] += 1
        '''
        if result == 0: print 'DRAW'
        elif result == 1: print 'WIN'
        else: print 'LOSE'
            '''
    continue
    s1_name = p1
    s2_name = p2
    print ''
    print s1_name +' VS '+s2_name
    print s1_name+'  win against '+s2_name+' : '+str(results[1])
    print s1_name+' lose against '+s2_name+' : '+str(results[2])
    print s1_name+' draw against '+s2_name+' : '+str(results[0])
    print ''
    ft = time.time()
    print 'EXECUTION TIME : '+str(int(ft-st))+'(s)'

