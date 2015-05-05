from abs_strategy import BaseStrategy

import time

class IterativeDeepening(BaseStrategy):

    def __init__(self, my_chara):
        super(IterativeDeepening, self).__init__(my_chara)
        self.MODE = 0
        self.LIMIT = 1
        self.TIME_LIMIT_MODE = 0
        self.DEPTH_LIMIT_MODE = 1
        self.COUNT = 0
        # variable for question detect 
        self.FLG_Q_FOUND = 123456789
        self.IS_DETECTING = True

    '''
    set strategy-specific parameter.
    mode  : the kind of computational budget for iterative deepening.
    limit : computational budget for iterative deepening.
    '''
    def setParameter(self, mode, limit):
        self.MODE = mode
        self.LIMIT = limit

    def makeANextMove(self, board):
        # concrete method of thinking process
        # return next move's row and column position.

        depth_limit = 0
        s_time = time.time()
        n_time = s_time
        alpha = -100
        beta  = 100
        solved = []
        scores = [0 for i in range(board.WIDTH)]
        search_counts = [0 for i in range(board.WIDTH)]

        while True:
            # If it reaches computational budget,
            # then stop searching and start to choose best move.
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
                # never choose full-stacked column as best move.
                # So assign very small score to this.
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

                # if find question, then write down it to question_data.txt and return flg.
                if temp_score > 0 and temp_score!= 36 and self.IS_DETECTING:
                    print ''
                    board.display()
                    return self.FLG_Q_FOUND

                if temp_score != 0:
                    solved.append(c)
                    scores[c] = temp_score
                else:
                    search_counts[c] = self.COUNT

            # If all calculation is done, search should finish.
            # But if you put aolumn 'n' and this leads the game draw,
            # then evalMove returns 0 and column n never appended to solved array.
            # So nevertheless we know the result , do not break searching loop
            # and depth_limit keep increasing.
            # To avoid this, we stop searching if depth_limit reaches to 42.
            if len(solved) == board.WIDTH or depth_limit == (board.WIDTH*board.HEIGHT):
                break

            # prepare to next DFS
            depth_limit += 1
            n_time = time.time()

        if self.D: print 'NOW DEPTH DEEPNESS:'+str(depth_limit)
        # get the column and row of best move
        best_score = max(scores)
        best_moves = []
        for c, score in enumerate(scores):
            if score == best_score:
                best_moves.append(c)
        if self.D:
            print 'SCORE:'+str(scores)
            print 'BEST SCORE:'+str(best_score)
            print 'BEST MOVE:'+str(best_moves)

        best_move = self.randomChoice(board, best_moves)
        return best_move

    def evalMove(self, depth_limit, depth, board, player, row, col, _alpha, _beta):
        # the score is evaluated by minimax tree rule.
        # this method is called recursively until
        # depth == n or finish the game.
        # shallower depth win (win in less steps) gets better score.
        alpha, beta = _alpha, _beta
        self.COUNT +=1

        if board.checkIfWin(player, row, col):
            if depth%2 == 0:
                return 36-depth
            elif depth%2 == 1:
                return -(36-depth)
        if depth == depth_limit:
            return 0

        next_player = self.ME if player == self.OPPO else self.OPPO
        best_score = 0
        is_first = True

        for c, r in enumerate(board.position):
            if r==board.HEIGHT:
                continue

            board.table[r][c] = next_player
            board.position[c] += 1
            temp_score = self.evalMove(depth_limit, depth+1, board, next_player, r, c, alpha, beta)
            board.table[r][c] = '-'
            board.position[c] -= 1

            if depth%2 == 0: # if this node is minimizer node
                if temp_score <= alpha: # or if temp_score < alpha
                    return temp_score
                if temp_score < beta:
                    beta = temp_score
            else: # if this node is maximizer node
                if temp_score >= beta: # or if temp_score < beta
                    return temp_score
                if temp_score > alpha:
                    alpha = temp_score

            if is_first:
                best_score = temp_score
                is_first = False
            elif depth%2 == 0: # next_player == USER -> choose min-score
                best_score = min(best_score, temp_score)
            else: # next_player == CPU -> choose max-score
                best_score = max(best_score, temp_score)

        return best_score
