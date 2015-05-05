import os
import sys

PARENT_PATH = os.getcwd()[:-4]
sys.path.append(PARENT_PATH+'ui')
sys.path.append(PARENT_PATH+'strategy')

import time
import copy
import board
import game_manager

import minimax_strategy
import alpha_beta_cut_strategy
import iterative_deepening_strategy

class GameSimulator:

    def __init__(self):
        # return value for each game result
        self.DRAW_POINT = 0
        self.WIN_POINT = 1
        self.LOSE_POINT = 2
        self.S1 = iterative_deepening_strategy.IterativeDeepening('O')
        self.S2 = iterative_deepening_strategy.IterativeDeepening('X')
        self.d = False # if (d == True) then display game progress on shell

    '''
    @param
    w : the return value you want when you win
    d : the return value you want when you draw
    l : the return value you want when you lose
    '''
    def setReturnValue(self, w, d, l):
        self.WIN_POINT = w
        self.DRAW_POINT = d
        self.LOSE_POINT = l

    '''
    *** argument ***
    s1 : strategy for first player
    s2 : strategy for second player
    *** return(default) ***
    result :
        0  : draw
        1  : first player win
        2 : second player win
        3 : found question
    '''
    def play(self, s1, s2):
        b = board.Board(4,7,6)
        t1, t2 = 0,0
        d = self.d
        turn = 0
        while(True):
            turn += 1
            st = time.time()
            col = s1.makeANextMove(b)
            if col == s1.FLG_Q_FOUND:
                s1.D = True
                s1.IS_DETECTING = False
                s1.makeANextMove(b)
                # ask if save this question
                print 'Save this question?(y/n)'
                flg = raw_input()
                if not (flg == 'y' or flg == 'Y'):
                    return self.DRAW_POINT
                json = self.convertQuestionToJson(b)
                # write json to data.txt
                with  open('data.txt','a+') as f:
                    f.write(json + '\n')
                return 3
            et = time.time()
            t1 += et-st
            is_cpu1_win = b.update(b.USER, col)
            if d: b.display()
            if is_cpu1_win:
                if d:print 'player1 average time:'+str(t1/(turn+1))
                if d:print 'player2 average time:'+str(t2/(turn))
                return self.WIN_POINT
            if b.checkIfDraw():
                if d:print 'player1 average time:'+str(t1/(turn+1))
                if d:print 'player2 average time:'+str(t2/(turn))
                return self.DRAW_POINT
            st = time.time()
            col = s2.think(b)
            et = time.time()
            t2 += et-st
            is_cpu2_win = b.update(b.CPU, col)
            if d: b.display()
            if is_cpu2_win:
                if d:print 'player1 average time:'+str(t1/(turn+1))
                if d:print 'player2 average time:'+str(t2/(turn))
                return self.LOSE_POINT
            if b.checkIfDraw():
                if d:print 'player1 average time:'+str(t1/(turn+1))
                if d:print 'player2 average time:'+str(t2/(turn))
                return self.DRAW_POINT
    '''
    **** Sample json format ****
    {
    "answer_moves":[4,5,1],
    "position":[0,0,2,2,0,0,0],
    "table":[[0,0,1,1,0,0,0],[0,0,-1,-1,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0]],
    "current_turn_num":0,
    "first_player":1,
    "limit_turn":3
    } 
    => current_turn_num is always 0 and first_player would also always 0.
    '''
    def convertQuestionToJson(self, board):
        pos = str(board.position)
        tb = str(self.convertTable(board.table))
        answer, turn = self.getAnswerPlay(board)
        json = '{'
        json += '"answer_moves":'+str(answer)+','
        json += '"position":'+pos+','
        json += '"table":'+tb+','
        json += '"current_turn_num":0,'
        json += '"first_player":1,'
        json += '"limit_turn":'+str(turn)+''
        json += '}'
        return json

    def convertTable(self, _tb):
        tb = copy.deepcopy(_tb)
        row = len(tb); col = len(tb[0])
        for r in range(row):
            for c in range(col):
                t = tb[r][c]
                tb[r][c] = 0 if t=='-' else 1 if t=='O' else -1
        return tb

    def getAnswerPlay(self, board):
        answer = []
        turn = 0
        while True:
            turn += 1
            col = self.S1.think(board)
            answer.append(col)
            if board.update(self.S1.ME, col): break
            turn += 1
            col = self.S2.think(board)
            answer.append(col)
            if board.update(self.S2.ME, col): break
        return answer, turn

