import random
'''
This class represents mutation phase in GA.
'''
class Mutation:

    def __init__(self, domain_knowledge):
        self.domain = domain_knowledge

    '''
    @param
        g : group of chromosomes
    @return
        new_g : group of chromosomes after mutation process
    '''
    def mutation(self, g):
        n = len(g)
        for i in range(n):
            for j in range(self.domain.CHROMO_LEN):
                if random.random() < self.domain.Pm:
                    #print j
                    #print bin(g[i])
                    mask = 1<<j
                    g[i] = g[i]^mask
                    #print bin(g[i])
        return g

