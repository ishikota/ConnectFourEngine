import os
import sys

PARENT_PATH = os.getcwd()[:-4]
sys.path.append(PARENT_PATH+'ui')
sys.path.append(PARENT_PATH+'strategy')
sys.path.append(PARENT_PATH+'GA/main')

import iterative_deepening_strategy
import game_simulator
import domain_knowledge
import csv
import random

simulator = game_simulator.GameSimulator()
simulator.D = True
s1 =  iterative_deepening_strategy.IterativeDeepening('O', 'X')
s2 =  iterative_deepening_strategy.IterativeDeepening('X', 'O')
s1.setParameter(s1.DEPTH_LIMIT_MODE, 4)
s2.setParameter(s2.DEPTH_LIMIT_MODE, 4)

# read parameter from csv file
data = 0
f_name = '../GA/data/best_chromos.csv'
with open(f_name, 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    #header = next(reader)  # do not read header
    for row in reader:
        data = row

# convert data(bit-array) into real value array.
D = domain_knowledge.Domain()
n =len(data)
for i in range(n):
    chromo = int(data[i])
    weights = D.chromoToDomainForm(chromo)
    data[i] = weights

# temp code
'''
n = 6
data = [0 for i in range(n)]
data[0] = [24, 18, 62, 0, 0, 0]
data[1] = [33, 3, 42, 32, 0, 0]
data[2] = [36, 3, 51, 7, 5, 7]
data[3] = [52, 29, 13, 28, 6, 51]
data[4] = [13, 59, 34, 38, 4, 54]
data[5] = [27, 36, 47, 51, 16, 42]
'''
# start test
print '--- START TEST (THE NUMBER OF TEST CHROMO IS '+str(n)+')---'
res = [0 for i in range(n)]
for i in range(n):
    print str(i+1)+'th test now ...'
    my_weight = data[i]
    s1.W1, s1.W2, s1.W3, s1.W4, s1.W5, s1.W6 = my_weight
    for j in range(10):
        #oppo_weight = data[random.randint(0,n-1)]
        #s2.W1, s2.W2, s2.W3, s2.W4, s2.W5, s2.W6 = oppo_weight
        result = simulator.play(s1, s2)
        result = -1 if result==2 else result
        res[i] += result

# sort result and get top N parameters.
for i in range(n):
    res[i] = (res[i], data[i])
res.sort()
res.reverse()
print ''
print '--- RANDOM MATCH RESULT ---'
print ''
for i in range(n):
    score = res[i][0]
    weight = res[i][1]
    print '('+str(i+1)+') score = '+str(score)+' : weight = '+str(weight)
print ''

#if n < 10:
#    raise Exception("Cannot held final match because member is less than 10.")
# final match with top 10 chromos.
#n = 10
print ''
print '--- TOP 10 FINAL MATCH ---'
for i in range(n):
    print 'No.'+str(i+1)+' : '+str(res[i][1])

# gives longer thinking time in final match
s1.setParameter(s1.DEPTH_LIMIT_MODE, 8)
s2.setParameter(s2.DEPTH_LIMIT_MODE, 8)

# table[i][j] : the result of No.i vs No.j
table = [[0 for j in range(n)] for i in range(n)]
for i in range(n):
    print str(i+1)+'th test now ...'
    my_weight = res[i][1]
    s1.W1, s1.W2, s1.W3, s1.W4, s1.W5, s1.W6 = my_weight
    for j in range(n):
        if i==j: continue
        oppo_weight = res[j][1]
        s2.W1, s2.W2, s2.W3, s2.W4, s2.W5, s2.W6 = oppo_weight
        result = simulator.play(s1, s2)
        result = -10 if result==2 else result
        table[i][j] = result
'''
print '--- RESULT TABLE ---'
for i in range(n):
    print '%2d %2d %2d %2d %2d %2d %2d %2d %2d %2d ' % (tuple(table[i]))
print ''
'''
res2 = [0 for i in range(n)]
for i in range(n):
    res2[i] = ( sum(table[i]), res[i][1])
res2.sort()
res2.reverse()
print '--- RANKING ---'
for i in range(n):
    score = res2[i][0]
    weight = res2[i][1]
    print '('+str(i+1)+') score = '+str(score)+' : weight = '+str(weight)

