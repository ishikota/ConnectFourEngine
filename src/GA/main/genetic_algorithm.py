import util
import domain_knowledge
import generation
import selection
import crossover
import mutation
from sys import stdout

'''
This class represents GA process.
Main program execute GA process through this class.
'''
class GA:

    def __init__(self):
        self.D = domain_knowledge.Domain()
        self.U = util.Util()

    def setParameter(self):
        pass

    def start(self):
        # init
        G = generation.Generation(self.D)
        S = selection.Selection(self.D)
        C = crossover.CrossOver(self.D)
        M = mutation.Mutation(self.D)

        # set parameter
        S.USE_SIGMA_SCALING = True
        C.USE_TWO_POINT_CROSSOVER = True

        g = G.createNewGroup(self.D.N)
        # array of average and best fitness value for each generation
        ave = [0 for i in range(self.D.GENERATION)]
        best = [0 for i in range(self.D.GENERATION)]

        print '';print '';print '';
        print ' [ First Generation ]'
        self.U.displayGeneration(g,self.D)
        for i in range(self.D.GENERATION):
            stdout.flush()
            stdout.write('\r [ %d/%d th Generation ]' % (i+1, self.D.GENERATION))
            self.D.refreshFVALMEMO()
            g = S.selectGoodChromos(g)
            g = C.crossOver(g)
            g = M.mutation(g)
            ave[i], best[i] = self.U.calcGenerationScore(g,self.D)
            if (i+1)%10==0:
                stdout.write('\n')
                self.U.displayGeneration(g,self.D)

        # write out best chromos for later use
        self.U.writeCSV('../data/best_chromos', g)

