
class Board:

    # initialize board size to width x height
    def __init__(self, connect_k, width, height):
        self.CONNECT_K = connect_k
        self.WIDTH = width
        self.HEIGHT = height
        self.table = [['-' for j in range(self.WIDTH)] for i in range(self.HEIGHT)]
        self.position = [0 for i in range(self.WIDTH)]
        self.USER = 'O'
        self.CPU = 'X'

    def display(self):
        # display table state to shell
        for row in reversed(range(self.HEIGHT)):
            line = '   '
            for col in range(self.WIDTH):
                line += self.table[row][col]+' '
            print line
        line = '   '
        for i in range(self.WIDTH):
            line +=str(i+1)+' '
        print line
        print ''

    def update(self, player, col):
        # update table state by putting new piece.
        # player : the kind of piece to put on the table (USER or CPU)
        # col    : the column to put the piece
        row = self.position[col]
        self.table[row][col] = player
        self.position[col] += 1
        return self.checkIfWin(player, row, col)

    def checkIfWin(self, player, row, col):
        # check if player win the game or not.
        # this method is called after player put
        # the pierce on table[row][col].
        # check 8 direction (do not need to check upper direction).

        # line_upper_right, line_horizontal, line_lower_right, line_bottom = 1,1,1,1
        line_nums = [1,1,1,1]
        di = [1,-1,0,0,-1,1,-1]
        dj = [1,-1,1,-1,1,-1,0]

        for d in range(7):
            line_num = 1
            ni, nj = row,col
            for k in range(3):
                ni += di[d]
                nj += dj[d]
                if not(0<=ni<self.HEIGHT) or not(0<=nj<self.WIDTH) or self.table[ni][nj] != player:
                    break
                line_nums[d/2] += 1
            if d%2==1 or d==6:
                if line_nums[d/2] >=self.CONNECT_K:
                    return True
        return False

    # if all columns are full stacked, it's draw game.
    def checkIfDraw(self):
        return self.position[0] == self.HEIGHT and len(set(self.position)) == 1

    def countWinningLine(self, player, row, col):
        # line_upper_right, line_horizontal, line_lower_right, line_bottom = 1,1,1,1
        line_nums = [1,1,1,1]
        line_component_nums = [0,0,0,0]
        threat_even_odd = [0,0,0,0] # flg-> 0:none, 1:odd, 2:even, 3:both
        di = [1,-1,0,0,-1,1,-1]
        dj = [1,-1,1,-1,1,-1,0]

        winning_line_num = 0
        winning_critical_line_num = 0
        best_component_num = 0
        odd_threat_num, even_threat_num = 0, 0
        opponent = self.CPU if player==self.USER else self.USER

        for d in range(6):
            ni, nj = row, col
            for k in range(3):
                ni += di[d]
                nj += dj[d]
                # if opponent is already interrupting this winning line
                if not(0<=ni<self.HEIGHT) or not(0<=nj<self.WIDTH) or self.table[ni][nj] == opponent:
                    break
                # if the square below the threat is not empty, then we do not count this winning line.
                # because opponent can immediately interrupt this threat.
                if ni==0 or (self.table[ni][nj] == '-' and self.table[ni-1][nj] != '-'):
                    break
                # if this square is threat, then check its even-odd and remember it.
                if self.table[ni][nj] == '-':
                    if ni%2==0: #this threat is odd-threat
                        threat_even_odd[d/2] |= 1
                    else: # this threat is even-threat
                        threat_even_odd[d/2] |= 2
                # if this winning line already has my pieces,
                # then you should fill this winning line.
                if self.table[ni][nj] == player:
                    line_component_nums[d/2] += 1
                line_nums[d/2] += 1
            if d%2==1:
                if line_nums[d/2] >= self.CONNECT_K:
                    winning_line_num += 1
                    best_component_num = max(best_component_num, line_component_nums[d/2])
                    if threat_even_odd[d/2] == 1:
                        odd_threat_num += 1
                    elif threat_even_odd[d/2] == 2:
                        even_threat_num += 1
                    # below code only concern about horizontal threat.
                    # The threat whose odd/even is mathces to the player is get large evaluation point.
                    # if d==3:
                    #     if (player=='O' and row%2==0) or (player=='X' and row%2==1):
                    #         winning_critical_line_num += 1
                    #         print 'Created critical threat'
        return winning_line_num, winning_critical_line_num,\
                best_component_num, odd_threat_num, even_threat_num

    # critical threat for first player is the threat placed in odd row.
    # critical threat for second player is the threat placed in even row.
    # this method returns,
    # array of (row, column) pair of critical threat which this move will create.
    def checkCriticalThreat(self, player, row, col):
        line_nums = [1,1,1,1]
        line_component_nums = [0,0,0,0]
        best_component_num = 0
        threat_even_odd = [0,0,0,0] # flg-> 0:none, 1:odd, 2:even, 3:both
        di = [1,-1,0,0,-1,1,-1]
        dj = [1,-1,1,-1,1,-1,0]
        # holds all threat here and if its critical one then move it to critical_pos array
        temp = [] 
        critical_pos = []

        opponent = self.CPU if player==self.USER else self.USER
        for d in range(6):
            ni,nj = row,col
            for k in range(self.CONNECT_K-1):
                ni += di[d]
                nj += dj[d]
                # if opponent is already interrupting this winning line
                if not(0<=ni<self.HEIGHT) or not(0<=nj<self.WIDTH) or self.table[ni][nj] == opponent:
                    break
                # if the square below the threat is not empty, then we do not count this winning line.
                # because opponent can immediately interrupt this threat.
                if ni==0 or (self.table[ni][nj] == '-' and self.table[ni-1][nj] != '-'):
                    break
                # if this square is threat, then check its even-odd and remember it.
                if self.table[ni][nj] == '-':
                    temp_pos.append((ni,nj))
                    if ni%2==0: #this threat is odd-threat
                        threat_even_odd[d/2] |= 1
                    else: # this threat is even-threat
                        threat_even_odd[d/2] |= 2
                # if this winning line already has my pieces,
                # then you should fill this winning line.
                if self.table[ni][nj] == player:
                    line_component_nums[d/2] += 1
                line_nums[d/2] += 1
            if d%2==1:
                if line_nums[d/2] >= self.CONNECT_K:
                    if (player == 'O' and threat_even_odd[d/2] == 1) or (player == 'X' and threat_even_odd[d/2] == 2):
                        critical_pos += temp_pos
                temp_pos = []
        return critical_pos

    def countLoosingLine(self, player, row, col):
        # line_upper_right, line_horizontal, line_lower_right, line_bottom = 1,1,1,1
        line_nums = [1,1,1,1]
        line_component_nums = [0,0,0,0]
        threat_even_odd = [0,0,0,0] # flg-> 0:none, 1:odd, 2:even, 3:both
        di = [1,-1,0,0,-1,1,-1]
        dj = [1,-1,1,-1,1,-1,0]
 
        loosing_line_num = 0
        loosing_critical_line_num = 0
        best_component_num = 0
        odd_threat_num, even_threat_num = 0, 0
        opponent = self.CPU if player==self.USER else self.USER

        for d in range(6):
            ni, nj = row, col
            for k in range(3):
                ni += di[d]
                nj += dj[d]
                # if ME already interrupted this loosing line
                if not(0<=ni<self.HEIGHT) or not(0<=nj<self.WIDTH) or self.table[ni][nj] == player:
                    break
                # if the square below the threat is not empty, do not need to be afraid of this loosing line.
                # because you can immediately interrupt this threat.
                if ni!=0 and self.table[ni][nj]=='-' and self.table[ni-1][nj] !='-':
                    break
                # if this square is threat, then check its even-odd and remember it.
                if self.table[ni][nj] == '-':
                    if ni%2==0: #this threat is odd-threat
                        threat_even_odd[d/2] |= 1
                    else: # this threat is even-threat
                        threat_even_odd[d/2] |= 2
                # if this loosing line already has its component,
                # then you should interrupt this line.(that's why count it)
                if self.table[ni][nj] == opponent:
                    line_component_nums[d/2] += 1
                line_nums[d/2] += 1
            if d%2==1:
                if line_nums[d/2] >= self.CONNECT_K:
                    loosing_line_num += 1
                    best_component_num = max(best_component_num, line_component_nums[d/2])
                    if threat_even_odd[d/2] == 1:
                        odd_threat_num += 1
                    elif threat_even_odd[d/2] == 2:
                        even_threat_num += 1

                    '''
                    # if this loosing line is critical for opponent then you should interupt this line very soon.
                    if d==3:
                        if (player=='O' and row%2==1) or (player=='X' and row%2==0):
                            loosing_critical_line_num += 1
                            print 'Killed critical threat'
                    '''

        return loosing_line_num, loosing_critical_line_num,\
                best_component_num, odd_threat_num, even_threat_num

    def setPlayer(self, user, cpu):
        self.USER = user
        self.CPU = cpu

    # reset board to initial state.
    def refresh(self):
        self.table = [['-' for j in range(self.WIDTH)] for i in range(self.HEIGHT)]
        self.position = [0 for i in range(self.WIDTH)]


