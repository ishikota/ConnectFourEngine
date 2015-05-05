from abs_strategy import BaseStrategy
import random
import copy
import math
import time
import iterative_deepening_strategy
import random_strategy
from sys import stdout

class Tree:
    def __init__(self, child_num):
        self.parent = -1
        self.childs = [-1 for i in range(child_num)]
        self.val = 0
        self.update_num = 0
        self.unvisited_child_num = child_num
        self.is_terminal = False

class BaseMCTS(BaseStrategy):

    def __init__(self, me):
        super(BaseMCTS, self).__init__(me)
        self.RANDOM_PLAYOUT = 0
        self.FUTURE_READ_PLAYOUT = 1
        self.PLAYOUT_POLICY = self.FUTURE_READ_PLAYOUT
        self.PLAYOUT_NUM = 50
        self.SEARCH_DEPTH = 2
        self.DD = False # flg : Debug Detail
        self.c = 0
        self.myRandomStrategy = random_strategy.RandomStrategy(self.ME)
        self.oppoRandomStrategy = random_strategy.RandomStrategy(self.OPPO)

    '''
    playout_policy : the policy how to choose next move in playout.
        RANDOM_PLAYOUT      : choose next move uniformly.
        FUTURE_READ_PLAYOUT : choose best move which gets highest score in iterative deepening.
    playout_num    : the number of times of playout to choose next move.
    search_depth   : computational budget for iterative deepening. never used in RANDOM_PLAYOUT.
    use_heuristic  : whether you use heuristic value in playout or not.(bool)
    '''
    def setParameter(self, playout_policy, playout_num, search_depth, use_heuristc):
        self.PLAYOUT_POLICY = playout_policy
        self.PLAYOUT_NUM = playout_num
        self.SEARCH_DEPTH = search_depth

        self.myStrategy = iterative_deepening_strategy.IterativeDeepening(self.ME)
        self.oppoStrategy = iterative_deepening_strategy.IterativeDeepening(self.OPPO)

        self.myStrategy.setParameter(self.myStrategy.DEPTH_LIMIT_MODE, search_depth)
        self.oppoStrategy.setParameter(self.oppoStrategy.DEPTH_LIMIT_MODE, search_depth)

        best_my_param = 24 if self.ME == 'O' else 1000
        best_oppo_param = 1000 if self.ME == 'X' else 24
        self.myStrategy.setHeuristicParameter(best_my_param,18,62,0,0,0)
        self.oppoStrategy.setHeuristicParameter(best_oppo_param,18,62,0,0,0)

        self.myStrategy.USE_HEURISTIC = use_heuristc
        self.oppoStrategy.USE_HEURISTIC = use_heuristc

    def makeANextMove(self, board):
        # concrete method of thinking process
        # return next move's row and column position.
        best_moves = self.UCTSearch(board)
        return [best_moves]

    # grow a MCTS tree and choose best root child.
    def UCTSearch(self, origin_board):
        # create root node v_0 with state s_0.
        v_0 = Tree(origin_board.WIDTH)
        v_0.is_root = True
        # iterate mcts search within computational budget
        play_counter = 0
        while play_counter < self.PLAYOUT_NUM:
            stdout.flush()
            stdout.write("\r  thinking...(%d/%d)" % (play_counter+1,self.PLAYOUT_NUM))
            cp_board = copy.deepcopy(origin_board)
            v_l, cp_board, next_player = self.treePolicy(v_0, cp_board)
            delta = self.defaultPolicy(v_l, cp_board, next_player)
            self.backUp(v_l, delta, next_player)
            play_counter += 1
        stdout.write("\n")
        # choose best child of root node.
        for child in v_0.childs:
            if child == -1 or child == -2: continue
            if self.D : print 'column:'+str(v_0.childs.index(child))+\
                    ' score:'+str(child.val)+' update:'+str(child.update_num)
        temp, best_action = self.bestChild(v_0, 0)
        return best_action

    '''
    *argument
    * v : root node of search tree
    * board : current state of child node which we are now focusing
    * return
    * v_l : leaf node of search tree
    * board : this board state is already updated to leaf node state.
    * next_player : next player to play after leaf node state
    '''
    def treePolicy(self, v, board):
        # while v is non-terminal node
        next_player = self.ME
        while not v.is_terminal:
            if v.unvisited_child_num != 0:
                return self.expand(v, board, next_player)
            else: # If all child nodes are visited, descends the tree toward best child node.
                c = 1.0/math.sqrt(2) # constant for adjustment
                v, column = self.bestChild(v,c)
                board.update(next_player, column)
                next_player = self.OPPO if next_player == self.ME else self.ME
        return v, board, next_player

    def expand(self, v, board, next_player):
        # choose un-tried action
        action = 0
        while True:
            action = v.childs.index(-1)
            v.unvisited_child_num -=1
            # if rest of un-tried action is infeasible(which make a move on full-stacked column),
            # this means that this node have already finished expanding process.
            # So jump to choose best-child process which we do after expanding process.
            if board.position[action] == board.HEIGHT:
                v.childs[action] = -2 # -2 indicates that this move is infeasible.
                if v.unvisited_child_num == 0:
                    return self.treePolicy(v, board)
            else:
                break
        # add a new child node to v
        v_child = Tree(len(v.childs))
        v_child.parent = v
        if board.update(next_player, action):
            v_child.is_terminal = True
            v_child.val = 1 if next_player == self.ME else -1
        elif board.checkIfDraw():
            v_child.is_terminal = True
            v_child.val = 0
        v.childs[action] = v_child
        next_player = self.OPPO if next_player == self.ME else self.ME
        return v_child, board, next_player

    # select a child which returns highest UCT value
    def bestChild(self, v, c):
        is_first = True
        best_val, best_index = -1000, -1
        for i in range(len(v.childs)):
            child = v.childs[i]
            UCTval = 0
            if child == -2: continue # if this action is infeasible, avoid choosing it(full-stacked move)
            try:
                exploitation_term = 1.0*child.val/child.update_num
                exploration_term = c*math.sqrt(2*math.log(v.update_num)/child.update_num)
                UCTval = exploitation_term + exploration_term
            except OverflowError,e:
                UCTval = float("inf")
            #print 'col:'+str(i)+' - UCT='+str(UCTval)
            if UCTval > best_val or is_first:
                best_val = UCTval
                best_index = i
                is_first = False
            elif UCTval == best_val:
                if bool(random.Random().getrandbits(1)): # probability of 1/2.
                    best_index = i
        return v.childs[best_index], best_index

    # do simulation and return a result value of simulation.
    def defaultPolicy(self, v_l, board, next_player):
        VAL_WIN,VAL_DRAW,VAL_LOSE = 1,0.5,0.01
        if v_l.is_terminal:
            return v_l.val
        while True:
            action = self.chooseNextMove(next_player, board)
            is_terminal = board.update(next_player, action)
            if is_terminal:
                return VAL_WIN if next_player == self.ME else VAL_LOSE
            elif board.checkIfDraw():
                return VAL_DRAW
            next_player = self.OPPO if next_player == self.ME else self.ME

    # backup the result score of simulation from leaf node to root node.
    def backUp(self, v, delta, next_player):
        # if v_l node is minimizer node, 
        # inverse sign of delta(reward) for negamax
        delta = -delta if next_player == self.ME else delta 
        while True: # ascends tree to the root node
            v.update_num += 1
            try:
                v.val += delta
            except OverflowError:
                if self.D:print 'OVERFLLOW!!'
            v = v.parent
            delta = -delta # doing negaMax here
            if v == -1:
                break

    # thie method chooses next move in playout
    def chooseNextMove(self, next_player, board):
        # use iterative deepening to select a next move
        if self.PLAYOUT_POLICY == self.FUTURE_READ_PLAYOUT:
            if next_player == self.ME:
                return self.myStrategy.think(board)
            else:
                return self.oppoStrategy.think(board)
        else:
            # random playout policy comes here
            if next_player == self.ME:
                return self.myRandomStrategy.think(board)
            else:
                return self.oppoRandomStrategy.think(board)


