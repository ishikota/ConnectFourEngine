import os
import sys

PARENT_PATH = os.getcwd()[:-4]
sys.path.append(PARENT_PATH+'ui')
sys.path.append(PARENT_PATH+'strategy')

import time
import game_manager

import iterative_deepening_strategy
import question_find_strategy
import question_detector
from sys import stdout

################################
# setting parameter here
FIND_DEPTH = 9
FIND_QUESTION_NUM = 10
################################

s1_depth = FIND_DEPTH; s2_depth = FIND_DEPTH-1
detector = question_detector.GameSimulator()
dev = '';
for i in range(50): dev += '='

print dev
print 'Start find question'
print 'FIND_DEPTH        = '+str(FIND_DEPTH)
print 'FIND_QUESTION_NUM = '+str(FIND_QUESTION_NUM)
print dev

temp = 0
for i in range(FIND_QUESTION_NUM):
    res = 0
    while res != 3:
        s1 = question_find_strategy.IterativeDeepening('O')
        s2 = iterative_deepening_strategy.IterativeDeepening('X')
        s1.setParameter(s1.DEPTH_LIMIT_MODE, s1_depth)
        s2.setParameter(s2.DEPTH_LIMIT_MODE, s1_depth)
        res = detector.play(s1, s2)
    stdout.flush()
    stdout.write('\r %d/%d questions found' % (i,FIND_QUESTION_NUM))
stdout.write('\n')
print 'END'
print dev
