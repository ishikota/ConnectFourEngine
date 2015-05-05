from abs_strategy import BaseStrategy
############################################
### DEPRECATED CLASS                       #
### Use IterativeDeepening class instead.  #
############################################
class MiniMax(BaseStrategy):

    def __init__(self, my_chara, oppo_chara):
        raise Exception, 'MiniMax class is deprecated. Use IterativeDeepening class instead.'
        super(MiniMax, self).__init__(my_chara, oppo_chara)
        self.MAX_DEPTH = 2

    # change strength by adjusting max_depth parameter.
    def setParameter(self, max_depth):
        self.MAX_DEPTH = max_depth

    def makeANextMove(self, board):
        # concrete method of thinking process
        # return next move's row and column position.
        scores = [0 for i in range(board.WIDTH)]
        #start_time = time.time()

        for c, r in enumerate(board.position):
            if r == board.HEIGHT:
                scores[c] = -1000
                continue

            board.table[r][c] = self.ME
            board.position[c] += 1
            scores[c] = self.evalMove(0, board, self.ME, r, c)
            board.table[r][c] = '-'
            board.position[c] -= 1

            if self.D: print '   score('+str(c+1)+') = '+str(scores[c])

        best_score = max(scores)
        best_moves = []
        for c, score in enumerate(scores):
            if score == best_score and board.position[c] != board.HEIGHT:
                best_moves.append(c)

        return best_moves

    def evalMove(self, depth, board, player, row, col):
        # the score is evaluated by minimax tree rule.
        # this method is called recursively until
        # depth == n or finish the game.
        # shallower depth win (win in less steps) gets better score.
        POSITIVE_PRIORITY_1 = 300
        POSITIVE_PRIORITY_2 = 200
        POSITIVE_PRIORITY_3 = 150
        NEGATIVE_PRIORITY_1 = -300
        NEGATIVE_PRIORITY_2 = -200
        NEGATIVE_PRIORITY_3 = -150
        POSITIVE_DOUBLE_REACH_VAL = 100
        NEGATIVE_DOUBLE_REACH_VAL = -100
        POSITIVE_NEXT_DOUBLE_REACH_VAL = 50
        NEGATIVE_NEXT_DOUBLE_REACH_VAL = -50

        if board.checkIfWin(player, row, col):
            if depth == 0:
                return POSITIVE_PRIORITY_1
            elif depth == 1:
                return NEGATIVE_PRIORITY_1
            elif depth == 2:
                return POSITIVE_DOUBLE_REACH_VAL
            elif depth == 3:
                return NEGATIVE_DOUBLE_REACH_VAL
            elif depth == 4:
                return POSITIVE_NEXT_DOUBLE_REACH_VAL
            elif depth == 5:
                return NEGATIVE_NEXT_DOUBLE_REACH_VAL
            elif depth%2 == 0:
                return 36-depth
            elif depth%2 == 1:
                return -(36-depth)
           
        if depth == self.MAX_DEPTH:
            return 0

        next_player = self.ME if player == self.OPPO else self.OPPO
        best_score = 0
        pos_double_reach_flg, nega_double_reach_flg = 0, 0
        pos_next_double_reach_flg, nega_next_double_reach_flg  = 0, 0
        is_first = True
        available_col = board.WIDTH
        
        #temp = 'depth:'+str(depth)+' '
        for c, r in enumerate(board.position):
            if r==board.HEIGHT:
                available_col -= 1
                continue

            board.table[r][c] = next_player
            board.position[c] += 1
            temp_score = self.evalMove(depth+1, board, next_player, r, c)
            board.table[r][c] = '-'
            board.position[c] -= 1

            if is_first:
                best_score = temp_score
                is_first = False
            elif depth%2 == 0: # next_player == USER -> choose min-score
                best_score = min(best_score, temp_score)
            else: # next_player == CPU -> choose max-score
                best_score = max(best_score, temp_score)

            if temp_score >= POSITIVE_DOUBLE_REACH_VAL:
                pos_double_reach_flg += 1
            #elif temp_score <= NEGATIVE_DOUBLE_REACH_VAL:
            #    nega_double_reach_flg += 1
            if temp_score >= POSITIVE_NEXT_DOUBLE_REACH_VAL:
                pos_next_double_reach_flg += 1
            #elif temp_score <= NEGATIVE_NEXT_DOUBLE_REACH_VAL:
            #    nega_next_double_reach_flg += 1

        #print temp
        #print 'depth:'+str(depth)+' best = '+str(best_score)
        if pos_double_reach_flg == available_col:
            return POSITIVE_PRIORITY_2
        #if nega_double_reach_flg == available_col:
        #    return NEGATIVE_PRIORITY_2
        if pos_next_double_reach_flg == available_col:
            return POSITIVE_PRIORITY_3
        #if nega_next_double_reach_flg == available_col:
        #    return NEGATIVE_PRIORITY_3

        return best_score
