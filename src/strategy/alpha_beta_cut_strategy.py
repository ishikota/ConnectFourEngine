from abs_strategy import BaseStrategy
############################################
### DEPRECATED CLASS                       #
### Use IterativeDeepening class instead.  #
############################################
class AlphaBetaCut(BaseStrategy):

    def __init__(self, my_chara, oppo_chara):
        super(AlphaBetaCut, self).__init__(my_chara)
        self.MAX_DEPTH = 2
        self.COUNT = 0

    # change strength by adjusting max_depth parameter.
    def setParameter(self, max_depth):
        self.MAX_DEPTH = max_depth

    def makeANextMove(self, board):
        # concrete method of thinking process
        # return next move's row and column position.
        self.COUNT = 0
        scores = [0 for i in range(board.WIDTH)]

        for c, r in enumerate(board.position):
            if r == board.HEIGHT:
                scores[c] = -100
                continue

            board.table[r][c] = self.ME
            board.position[c] += 1
            temp_score = self.evalMove(0, board, self.ME, r, c, -100, 100)
            board.table[r][c] = '-'
            board.position[c] -= 1

            if self.D: # id debug mode
                print '   score('+str(c+1)+') = '+str(temp_score)
                print 'COUNT:'+str(self.COUNT)
            scores[c] = temp_score

        best_score = max(scores)
        best_moves = []
        for c, score in enumerate(scores):
            if score == best_score and board.position[c] != board.HEIGHT:
                best_moves.append(c)

        return best_moves

    def evalMove(self, depth, board, player, row, col, _alpha, _beta):
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
        if depth == self.MAX_DEPTH:
            return 0

        next_player = self.ME if player == self.OPPO else self.OPPO
        best_score = 0
        is_first = True
        
        for c, r in enumerate(board.position):
            if r==board.HEIGHT:
                continue

            board.table[r][c] = next_player
            board.position[c] += 1
            temp_score = self.evalMove(depth+1, board, next_player, r, c, alpha, beta)
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
