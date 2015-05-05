import os
import sys
PARENT_PATH = os.getcwd()[:-7]
sys.path.append(PARENT_PATH+'ui')
sys.path.append(PARENT_PATH+'strategy')
sys.path.append(PARENT_PATH+'test')
import board
import iterative_deepening_strategy
import game_simulator
import random

'''
This class holds domain specific parameters for GA.
Write these methods to fit your problem.
    * chromoToDomainForm(chromo) : convert chromosome(bit form) into your domain specific form here
    * fitnessFunction(chromo) : evaluate passed chromosome by positive number.
And you can rewrite Util.displayChromo(chromo, domain) to display progress of GA as your like format.
'''
class Domain:

    def __init__(self):
        self.GENERATION = 10 # the number of generation during GA
        self.N = 3 # the number of chromosome in a generation.
        self.CHROMO_LEN = 36 # the length of chromosome's body
        self.Pc = 0.5 # probability of cross over occurs
        self.Pm = 0.01 # probability of mutation happens
        self.FVAL_MEMO = {} # memo of fitness value of chromo in a generation

    '''
    convert chromosomes' expression from bit array into actual value for domain.
    chromo is 36 bit length of bit array.
    each 6 bit represents value of corresponding weight.
    like first 6 bit corresponds to W1 and second is W2 and ...
    '''
    def chromoToDomainForm(self, chromo):
        #print 'bin'+bin(chromo)
        mask = (1<<6)-1
        weights = [0 for i in range(6)]
        for i in range(6):
            weights[i] = (chromo&mask)
            chromo = chromo>>6
        #print 'w'+str(weights)
        return weights

    # refresh FVAL_MEMO in when new generation starts.
    def refreshFVALMEMO(self):
        self.FVAL_MEMO = {}

    def fitnessFunction(self, *args):
        if len(args) == 1:
            return self.fitnessFunction1(args[0])
        if len(args) == 2:
            return self.fitnessFunction2(args[0], args[1])

    '''
    write your domain specific fitness function here.
    f_val should be positive number.
    @param
        chromo  : chromosome to evaluate. chromosome is bit-array
    @return
        f_val   : fitness value of chromosome.
    '''
    def fitnessFunction1(self,chromo):
        # if chromo is already evaluated,
        # then return the value you before evaluated.
        if chromo in self.FVAL_MEMO:
            return self.FVAL_MEMO[chromo]

        # init game environment
        b = board.Board(4, 7, 6)
        s1 = iterative_deepening_strategy.IterativeDeepening(b.USER)
        s2 = iterative_deepening_strategy.IterativeDeepening(b.CPU)
        s1.setParameter(s1.DEPTH_LIMIT_MODE, 6)
        s2.setParameter(s2.DEPTH_LIMIT_MODE, 6)
        s1.USE_HEURISTIC = True
        s2.USE_HEURISTIC = True
        WIN_REWARD , DRAW_REWARD , LOSE_REWARD = 5, 1, 0.5
        simulator = game_simulator.GameSimulator()
        simulator.setReturnValue(WIN_REWARD, DRAW_REWARD, LOSE_REWARD)

        # change weights of heuristic function following by chromo
        s1.W1,s1.W2,s1.W3,s1.W4,s1.W5,s1.W6 = self.chromoToDomainForm(chromo)

        f_val = 0
        # simulate the game for 3 times
        for i in range(3):
            f_val += simulator.play(s1, s2)

        self.FVAL_MEMO[chromo] = f_val
        return f_val


    def fitnessFunction2(self,my_chromo, oppo_chromos):
        # if chromo is already evaluated,
        # then return the value you before evaluated.
        if my_chromo in self.FVAL_MEMO:
            return self.FVAL_MEMO[my_chromo]

        # init game environment
        b = board.Board(4, 7, 6)
        s1 = iterative_deepening_strategy.IterativeDeepening(b.USER)
        s2 = iterative_deepening_strategy.IterativeDeepening(b.CPU)
        s1.setParameter(s1.DEPTH_LIMIT_MODE, 3)
        s2.setParameter(s2.DEPTH_LIMIT_MODE, 3)
        WIN_REWARD , DRAW_REWARD , LOSE_REWARD = 5, 1, 0.5
        simulator = game_simulator.GameSimulator()
        simulator.setReturnValue(WIN_REWARD, DRAW_REWARD, LOSE_REWARD)

        # change weights of heuristic function following by chromo
        s1.W1,s1.W2,s1.W3,s1.W4,s1.W5,s1.W6 = self.chromoToDomainForm(my_chromo)

        f_val = 0
        # simulate the game for 3 times
        for i in range(3):
            oppo_chromo = random.choice(oppo_chromos)
            s2.W1,s2.W2,s2.W3,s2.W4,s2.W5,s2.W6 = self.chromoToDomainForm(oppo_chromo)
            f_val += simulator.play(s1, s2)

        self.FVAL_MEMO[my_chromo] = f_val
        return f_val


