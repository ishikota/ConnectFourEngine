import random

'''
This class represents selection phase in GA.
'''
class CrossOver:

    def __init__(self, domain_knowledge):
        self.domain = domain_knowledge
        self.USE_TWO_POINT_CROSSOVER = False
    '''
    main process of cross over.
    @param
        g     : group to crossover
    @return
        new_g : new group after crossover
    '''
    def crossOver(self, g):
        n = len(g)
        new_g = [-1 for i in range(n)] 
        array = [-1 for i in range(n+1)] # positions of chromos to be paren
        counter = 0 # count the number of parent to be cross over

        for i in range(n):
            new_g[i] = g[i] # copy chromos to new group here
            if random.random() < self.domain.Pc:
                array[counter] = i
                counter += 1
        # if the number of parent is odd, add one more parent randomly
        if counter%2==1:
            array[counter] = random.randint(0,n-1)
            counter += 1
        if counter%2!=0:raise Exception("crossover : odd parent choosen")

        # do cross over and remove parents and add childs to group.
        for i in range(counter/2):
            i1, i2 = array[2*i], array[2*i+1]
            c1, c2 = 0, 0
            if self.USE_TWO_POINT_CROSSOVER:
                c1, c2 = self.twoPointCrossOver(g[i1], g[i2])
            else:
                c1,c2 = self.onePointCrossOver(g[i1], g[i2])
            new_g[i1], new_g[i2] = c1, c2 # swap childs and parents in new group

        return new_g

    '''
    do cross over by using two parent which are passed in argument
    and return new chromosome.
    '''
    def onePointCrossOver(self, p1, p2):
        # c_pos : cross over position of bit array.
        # if p1 = 11101010, p2=00110101 and c_pos = 3,
        # then child1 and child2 are...
        # child1 = 00110|010
        # child2 = 11101|101
        c_pos = random.randint(1,self.domain.CHROMO_LEN-1)
        p1_mask = (1<<c_pos)-1
        p2_mask = ((1<<self.domain.N)-1)^p1_mask
        child1 = p1&p1_mask|p2&p2_mask
        child2 = p2&p1_mask|p1&p2_mask
        if False: # debug code
            print bin(p1)
            print bin(p2)
            print bin(child1)
            print bin(child2)
        return child1, child2

    def twoPointCrossOver(self, p1, p2):
        # pos_r : crossover position of right side (0<=val<=n)
        # pos_l : crossover position of left side
        # if p1 = 11101010, p2=00110101 and
        # c_pos_l = 2 abd c_pos_r = 5
        # then child1 and child2 are...
        # child1 = 111|101|10
        # child2 = 001|010|01
        n = self.domain.CHROMO_LEN
        tmp1 = random.randint(0,n)
        tmp2 = random.randint(0,n)
        pos_l = max(tmp1, tmp2)
        pos_r = min(tmp1, tmp2)
        r_mask = (1<<pos_r)-1
        m_mask = ((1<<(pos_l-pos_r))-1)<<pos_r
        l_mask = ((1<<(n-pos_l))-1)<<pos_l
        child1 = p1&l_mask|p2&m_mask|p1&r_mask
        child2 = p2&l_mask|p1&m_mask|p2&r_mask
        if False: # debug code
            print pos_r, pos_l
            print bin(child1)
            print bin(child2)
        return child1, child2
