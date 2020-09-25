import numpy as np
import random
import time

COLOR_BLACK=-1
COLOR_WHITE=1
COLOR_NONE=0

class AI(object):

    value_table=np.array([
    [20, -3, 11, 8, 8, 11, -3, 20],
    [-3, -7, -4, 1, 1, -4, -7, -3],
    [11, -4, 2, 2, 2, 2, -4, 11],
    [8, 1, 2, -3, -3, 2, 1, 8],
    [8, 1, 2, -3, -3, 2, 1, 8],
    [11, -4, 2, 2, 2, 2, -4, 11],
    [-3, -7, -4, 1, 1, -4, -7, -3],
    [20, -3, 11, 8, 8, 11, -3, 20]
    ])

    MAX_DEPTH=3

    MAX_INT=666666
    MIN_INT=-666666

    def __init__(self, chessboard_size, color, time_out):
        self.chessboard_size=chessboard_size
        self.color=color
        self.time_out=time_out
        self.candidate_list=[]

    def go(self, chessboard):
        self.candidate_list.clear()

        self.find_all_pos(chessboard, self.color, self.candidate_list)

        if self.candidate_list:
            maxpos=self.candidate_list[0]
            maxvalue=self.evaluate(chessboard, self.color, AI.MIN_INT, maxpos, 0)
            for i in range(1, len(self.candidate_list)):
                tempvalue=self.evaluate(chessboard, self.color, maxvalue, self.candidate_list[i], 0)
                if tempvalue>maxvalue:
                    maxpos=self.candidate_list[i]
                    maxvalue=tempvalue
            self.candidate_list.append(maxpos)

    def find_all_pos(self, chessboard, color, li):
        emptypos=np.where(chessboard==COLOR_NONE)
        emptypos=list(zip(emptypos[0], emptypos[1]))
        for pos in emptypos:
            self.check(chessboard, color, li, pos)

    def check(self, chessboard, color, li, coord):    
        for i in (0, 1, -1):
            for j in (0, 1, -1):
                if (i, j)==(0, 0):
                    continue
                else:
                    flag=False
                    for step in range(1, 8):
                        currentpos=(coord[0]+step*i, coord[1]+step*j)
                        if currentpos[0]>7 or currentpos[0]<0 or currentpos[1]>7 or currentpos[1]<0:
                            break
                        elif chessboard[currentpos]==COLOR_NONE:
                            break
                        elif chessboard[currentpos]==-color:
                            flag=True
                        elif chessboard[currentpos]==color:
                            if flag:
                                li.append(coord)
                                return
                            break
    
    def flip(self, chessboard, color, pos):
        tempboard=chessboard.copy()
        tempboard[pos]=color
        for i in (0, 1, -1):
            for j in (0, 1, -1):
                if (i, j)==(0, 0):
                    continue
                else:
                    flag=False
                    for step in range(1, 8):
                        currentpos=(pos[0]+step*i, pos[1]+step*j)
                        if currentpos[0]>7 or currentpos[0]<0 or currentpos[1]>7 or currentpos[1]<0:
                            break
                        elif tempboard[currentpos]==COLOR_NONE:
                            break
                        elif tempboard[currentpos]==-color:
                            flag=True
                        elif tempboard[currentpos]==color:
                            if flag:
                                for k in range(1, step):
                                    tempboard[pos[0]+k*i][pos[1]+k*j]*=-1
                            break
        return tempboard

    def evaluate(self, chessboard, color, current_level_value, pos, depth):
        if depth>AI.MAX_DEPTH:
            return 0

        tempboard=self.flip(chessboard, color, pos)
        calculated_value=AI.value_table[pos]
        value=calculated_value if color==self.color else -calculated_value

        # print(tempboard)

        templist=[]
        self.find_all_pos(tempboard, -color, templist)

        maxvalue=AI.MIN_INT
        minvalue=AI.MAX_INT

        if color==self.color:
            for p in templist:
                tempvalue=self.evaluate(tempboard, -color, minvalue, p, depth+1)
                if value+tempvalue<=current_level_value:
                    return AI.MIN_INT
                if tempvalue<minvalue:
                    minvalue=tempvalue
        else:
            for p in templist:
                tempvalue=self.evaluate(tempboard, -color, maxvalue, p, depth+1)
                if value+tempvalue>=current_level_value:
                    return AI.MAX_INT
                if tempvalue>maxvalue:
                    maxvalue=tempvalue
            
        delta=maxvalue if color==-self.color else minvalue

        # print(value+delta if color==self.color else -value+delta)

        return value+delta

if __name__ == "__main__":
    ai=AI(8, 1, 30)
    cb=np.array([[0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 1, -1, 0, 0, 0],
                 [0, 0, 0, -1, 1, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0]])

    te=np.array([[0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 1, 0, 1, -1, 0, 0, 0],
                 [0, 1, -1, -1, -1, -1, 0, 0],
                 [0, -1, 1, 1, -1, 0, 0, 0],
                 [0, 0, 0, -1, 1, 0, 0, 0],
                 [0, 0, 0, 1, 1, -1, 0, 0],
                 [0, 0, 1, 0, 1, 0, 0, 0],
                 [0, 1, -1, -1, 0, 1, 0, 0]])
    ai.go(te)
    print(ai.candidate_list)