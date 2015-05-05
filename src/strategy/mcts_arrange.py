from abs_strategy import BaseStrategy
from mcts_base import BaseMCTS
from mcts_base import Tree
from iterative_deepening_strategy import IterativeDeepening
import copy
import time
from sys import stdout

'''
TunedMCTS is subclass of BaseMCTS which added below features to improve strength.
1. added PruneLoseMove method to avoid searching meaningless move.
2. this strategy uses randomstrategy with strong heuristic in playout.
'''
class TunedMCTS(BaseMCTS):

    def __init__(self, me):
        super(TunedMCTS, self).__init__(me)
        # init const
        self.MODE_TIME_LIMIT = 0
        self.MODE_PLAYOUT_NUM_LIMIT = 1
        self.PLAYOUT_MODE = self.MODE_PLAYOUT_NUM_LIMIT
        self.COMPUTATION_BUDGET = 100

        # init prune strategy
        self.PRUNE_DEPTH = 8
        self.PruneStrategy = PruneStrategy(self.ME)
        self.PruneStrategy.setParameter(self.PruneStrategy.DEPTH_LIMIT_MODE, self.PRUNE_DEPTH)
        self.PruneStrategy.USE_HEURISTIC = False

        # init random strategy for playout
        self.PLAYOUT_POLICY = self.RANDOM_PLAYOUT
        self.myRandomStrategy.USE_STRONG_HEURISTIC = True
        self.oppoRandomStrategy.USE_STRONG_HEURISTIC = True
        self.myRandomStrategy.USE_HEURISTIC = False
        self.oppoRandomStrategy.USE_HEURISTIC = False
        # (24,18,62,0,0,0) is best parameter for first player
        # (1000,18,62,0,0,0) is best parameter for second player
        if me=='O':
            self.myRandomStrategy.setHeuristicParameter(24,18,62,0,0,0)
            self.oppoRandomStrategy.setHeuristicParameter(1000,18,62,0,0,0)
        else:
            self.myRandomStrategy.setHeuristicParameter(1000,18,62,0,0,0)
            self.oppoRandomStrategy.setHeuristicParameter(24,18,62,0,0,0)

    def setParameter(self, flg_playout_limit, playout_limit, prune_depth):
        self.PLAYOUT_MODE = flg_playout_limit
        self.COMPUTATION_BUDGET = playout_limit
        self.PRUNE_DEPTH = prune_depth
        self.PruneStrategy.setParameter(self.PruneStrategy.DEPTH_LIMIT_MODE, self.PRUNE_DEPTH)


    # grow a MCTS tree and choose best root child.
    def UCTSearch(self, origin_board):
        # create root node v_0 with state s_0.
        v_0 = Tree(origin_board.WIDTH)
        v_0.is_root = True

        # prune moves by iterative deepening.
        # if winning move found, then do not do MCTS search.
        best_moves = self.pruneLoseMove(origin_board, v_0)
        if best_moves != -1:
            return best_moves[0]

        play_counter = 0; st = time.time(); et = st; budget = 0
        while True:
            stdout.flush()

            # iterate mcts search within computational budget
            if self.PLAYOUT_MODE == self.MODE_TIME_LIMIT:
                budget = et-st
                stdout.write("\r  thinking...(%f/%f)" % (et-st, self.COMPUTATION_BUDGET))
            else:
                budget = play_counter
                stdout.write("\r  thinking...(%d/%d)" % (play_counter, self.COMPUTATION_BUDGET))
            if budget >= self.COMPUTATION_BUDGET: 
                break

            cp_board = copy.deepcopy(origin_board)
            v_l, cp_board, next_player = self.treePolicy(v_0, cp_board)
            delta = self.defaultPolicy(v_l, cp_board, next_player)
            self.backUp(v_l, delta, next_player)
            play_counter += 1
            et = time.time()

        stdout.write("\n")
        # choose best child of root node.
        for child in v_0.childs:
            if child == -1 or child == -2: continue
            if self.D : print 'column:'+str(v_0.childs.index(child))+\
                    ' score:'+str(child.val)+' update:'+str(child.update_num)
        temp, best_action = self.bestChild(v_0, 0)
        return best_action

    # change the move state which we know it will lose to terminal node
    # not to search this move later.
    # if found winning move in PruneStrategy, then return them.
    # (because we do not need to search anymore)
    def pruneLoseMove(self, board, v_0):
        possible_columns = []
        best_moves,best_score = self.PruneStrategy.makeANextMove(board)

        # if winning move found then return them.
        if best_score!=0: return best_moves
        #if best_score>0: return best_moves

        for col in range(board.WIDTH):
            if board.position[col] == board.HEIGHT:
                continue
            if col not in best_moves:
                v_0.unvisited_child_num -=1
                v_child = Tree(len(v_0.childs))
                v_child.parent = v_0
                v_child.is_terminal = True
                v_child.val = -10
                v_child.update_num = 1
                v_0.childs[col] = v_child

        return -1



# This class is almost same to IterativeDeepening.
# only difference is return value of makeANextMove method.
# this method returns best_score which is used in 
# avobe method 'pruneLoseMove'
class PruneStrategy(IterativeDeepening):
     def makeANextMove(self, board):
        depth_limit = 0
        s_time = time.time()
        n_time = s_time
        alpha = -100
        beta  = 100
        solved = []
        scores = [0 for i in range(board.WIDTH)]
        search_counts = [0 for i in range(board.WIDTH)]

        while True:
            budget = 0
            if self.MODE == self.TIME_LIMIT_MODE:
                budget = n_time - s_time
            else:
                budget = depth_limit
            if budget >= self.LIMIT:
                break

            fullStackedNum = 0
            for c, r in enumerate(board.position):
                self.COUNT = 0
                if c in solved:
                    continue
                if r == board.HEIGHT:
                    fullStackedNum += 1
                    scores[c] = -100
                    solved.append(c)
                    continue

                board.table[r][c] = self.ME
                board.position[c] += 1
                temp_score = self.evalMove(depth_limit, 0, board, self.ME, r, c, alpha, beta)
                board.table[r][c] = '-'
                board.position[c] -= 1

                if temp_score != 0:
                    solved.append(c)
                    scores[c] = temp_score
                else:
                    search_counts[c] = self.COUNT

            if len(solved) == board.WIDTH or depth_limit ==37:
                break

            depth_limit += 1
            n_time = time.time()

        if self.D: print 'NOW DEPTH DEEPNESS:'+str(depth_limit)
        # get the column and row of best move
        best_score = max(scores)
        best_moves = []
        for c, score in enumerate(scores):
            if score == best_score:
                best_moves.append(c)
        return best_moves, best_score




