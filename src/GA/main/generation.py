import random
'''
This class represents generation phase in GA
'''
class Generation:

    def __init__(self, domain_knowledge):
        self.domain = domain_knowledge

    '''
    create new group of chromosome.
    @param
        chromo_num    : the number of chromosome in this generation.
    @return
        generation : the array of chromosomes.
    '''
    def createNewGroup(self, chromo_num):
        g = [0 for i in range(chromo_num)]
        for i in range(chromo_num):
            g[i] = self.createNewChromo()
        return g

    '''
    Create new chromosome and return it.
    chromosome is represented as bit array.
    the length of chromosome body is defined in domain_knowledge.py.
    @return
        chromo : new chromosome.
    '''
    def createNewChromo(self):
        return random.randint(0, (1<<self.domain.CHROMO_LEN)-1)

