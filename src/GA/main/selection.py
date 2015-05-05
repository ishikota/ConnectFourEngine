import math
import random
'''
This class represents selection phase in GA.
'''
class Selection:
 
    def __init__(self, domain_knowledge):
        self.domain = domain_knowledge
        self.USE_SIGMA_SCALING = False

    '''
    @param
        g     : group of chromosomes which will be selected.
    @return
        new_g : chromosomes which are selected in selection process.
    '''
    def selectGoodChromos(self, g):
        s = len(g)
        new_g = [0 for i in range(s)]
        q = self.calcCumulativeProb(g)
        for i in range(s):
            r = random.random()
            for j in range(s):
                if r<=q[j]:
                    new_g[i] = g[j]
                    break
        return new_g

    '''
    calculate cumulative probability which we use in roulette selection
    '''
    def calcCumulativeProb(self, g):
        s = len(g)
        F = 0 # sum of all chromosome's fitness value
        f = [0 for i in range(s)] # fitness value of chromosomes
        p = [0 for i in range(s)] # probability of selection of chromosomes
        q = [0 for i in range(s)] # cumulative probability of chromosomes

        # calculate fitness value
        for i in range(s):
            f[i] = self.domain.fitnessFunction(g[i], g)
        
        if self.USE_SIGMA_SCALING:
            f = self.sigmaScaling(f)

        # calculate probability of selection
        F = sum(f)
        for i in range(s):
            p[i] = 1.0*f[i]/F
        # calculate cumulative probability
        q[0] = p[0]
        for i in range(1,s):
            q[i] = q[i-1] + p[i]

        return q
    
    '''
    @param
        f : array of fitness value in a group.
    @return
        scaled_f : array of fitness value scaled by this function.
    '''
    def sigmaScaling(self, f):
        n = len(f)
        f_ave = sum(f)*1.0/n
        sigma = self.calcStandardDeviation(f)
        scaled_f = [0 for i in range(n)]
        for i in range(n):
            if sigma == 0:
                scaled_f[i] = 1.0
            else:
                scaled_f[i] = 1 + (f[i]-f_ave) / (2*sigma)
        return scaled_f

    # calculate standard deviation of set of numberes(val).
    def calcStandardDeviation(self, val):
        n = len(val)
        ave = 1.0*sum(val)/n
        ans = 0
        for i in range(n):
            ans += (val[i]-ave)**2
        ans = ans/n
        ans = math.sqrt(ans)
        return ans

