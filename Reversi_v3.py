import numpy as np
import random
import time

COLOR_BLACK=-1
COLOR_WHITE=1
COLOR_NONE=0

class AI(object):

    value_table=np.array([
    [999, -3, 11, 8, 8, 11, -3, 999],
    [-3, -7, -4, 1, 1, -4, -7, -3],
    [11, -4, 2, 2, 2, 2, -4, 11],
    [8, 1, 2, -3, -3, 2, 1, 8],
    [8, 1, 2, -3, -3, 2, 1, 8],
    [11, -4, 2, 2, 2, 2, -4, 11],
    [-3, -7, -4, 1, 1, -4, -7, -3],
    [999, -3, 11, 8, 8, 11, -3, 999]
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
            if self.countstep(chessboard)<8:
                self.candidate_list.append(self.candidate_list[random.randint(0, len(self.candidate_list)-1)])
            else:
                maxpos=self.candidate_list[0]
                maxvalue=self.get_value(chessboard, AI.MIN_INT, maxpos)
                for i in range(1, len(self.candidate_list)):
                    tempvalue=self.get_value(chessboard, maxvalue, self.candidate_list[i])
                    if tempvalue>maxvalue:
                        maxpos=self.candidate_list[i]
                        maxvalue=tempvalue
                self.candidate_list.append(maxpos)

    def countstep(self, chessboard):
        allchess=np.where(chessboard!=COLOR_NONE)
        allchess=list(zip(allchess[0], allchess[1]))
        return len(allchess)

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

    def count_stable(self, chessboard, color):
        count=0
        current_chess=np.where(chessboard==color)
        current_chess=list(zip(current_chess[0], current_chess[1]))
        for pos in current_chess:
            if self.is_stable(chessboard, color, pos):
                count+=1
        return count

    def is_stable(self, chessboard, color, pos):
        flag1_1=True; flag1_2=True
        flag2_1=True; flag2_2=True
        flag3_1=True; flag3_2=True
        flag4_1=True; flag4_2=True

        for i in range(1, 8):
            temppos=(pos[0], pos[1]+i)
            if (temppos[1]>7):
                break
            if chessboard[temppos]!=color:
                flag1_1=False
                break
        for i in range(1, 8):
            temppos=(pos[0], pos[1]-i)
            if (temppos[1]<0):
                break
            if chessboard[temppos]!=color:
                flag1_2=False
                break

        for i in range(1, 8):
            temppos=(pos[0]+i, pos[1])
            if (temppos[0]>7):
                break
            if chessboard[temppos]!=color:
                flag2_1=False
                break
        for i in range(1, 8):
            temppos=(pos[0]-i, pos[1])
            if (temppos[0]<0):
                break
            if chessboard[temppos]!=color:
                flag2_2=False
                break

        for i in range(1, 8):
            temppos=(pos[0]+i, pos[1]+i)
            if (temppos[1]>7 or temppos[0]>7):
                break
            if chessboard[temppos]!=color:
                flag3_1=False
                break
        for i in range(1, 8):
            temppos=(pos[0]-i, pos[1]-i)
            if (temppos[1]<0 or temppos[0]<0):
                break
            if chessboard[temppos]!=color:
                flag3_2=False
                break

        for i in range(1, 8):
            temppos=(pos[0]+i, pos[1]-i)
            if (temppos[1]<0 or temppos[0]>7):
                break
            if chessboard[temppos]!=color:
                flag4_1=False
                break
        for i in range(1, 8):
            temppos=(pos[0]-i, pos[1]+i)
            if (temppos[1]>7 or temppos[0]<0):
                break
            if chessboard[temppos]!=color:
                flag4_2=False
                break

        return (flag1_1 or flag1_2) and (flag2_1 or flag2_2) and (flag3_1 or flag3_2) and (flag4_1 or flag4_2)
        
    def count_diffu(self, chessboard, color):
        count=0
        current_chess=np.where(chessboard==color)
        current_chess=list(zip(current_chess[0], current_chess[1]))
        for pos in current_chess:
            if self.is_diffu(chessboard, pos):
                count+=1
        return count
            
    def is_diffu(self, chessboard, pos):
        if pos[0]==7 or pos[0]==0 or pos[1]==7 or pos[1]==0:
            return False
        for i in (0, 1, -1):
            for j in (0, 1, -1):
                if (i, j)==(0, 0):
                    continue
                else:
                    temppos=(pos[0]+i, pos[1]+j)
                    if chessboard[temppos]==COLOR_NONE:
                        return True
    
    def is_sb(self, chessboard, color, pos):
        if chessboard[pos]!=color:
            return 0
        if pos[0]==7 or pos[0]==0:
            temppos=(pos[0], pos[1]+1)
            if not (temppos[0]>7 or temppos[0]<0 or temppos[1]>7 or temppos[1]<0):
                if chessboard[temppos]==-color:
                    return 1
            temppos=(pos[0], pos[1]-1)
            if not (temppos[0]>7 or temppos[0]<0 or temppos[1]>7 or temppos[1]<0):
                if chessboard[temppos]==-color:
                    return 1
        elif pos[1]==7 or pos[1]==0:
            temppos=(pos[0]+1, pos[1])
            if not (temppos[0]>7 or temppos[0]<0 or temppos[1]>7 or temppos[1]<0):
                if chessboard[temppos]==-color:
                    return 1
            temppos=(pos[0]-1, pos[1])
            if not (temppos[0]>7 or temppos[0]<0 or temppos[1]>7 or temppos[1]<0):
                if chessboard[temppos]==-color:
                    return 1
        return 0

    def evaluate(self, chessboard, color, current_level_value, pos, depth):
        if depth>AI.MAX_DEPTH:
            return 0

        tempboard=self.flip(chessboard, color, pos)
        # print(tempboard)
        templist=[]
        self.find_all_pos(tempboard, -color, templist)

        calculated_value=AI.value_table[pos]*2-self.count_diffu(tempboard, color)*3+self.count_stable(tempboard, color)*10
        value=calculated_value if color==self.color else -calculated_value

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
    
    def get_value(self, chessboard, clv, pos):
        v=self.evaluate(chessboard, self.color, clv, pos, 0)
        # tempboard=self.flip(chessboard, self.color, pos)
        # v=v-self.is_sb(tempboard, self.color, pos)*1000
        return v

if __name__ == "__main__":
    ai=AI(8, -1, 30)
    cb=np.array([[0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 1, -1, 0, 0, 0],
                 [0, 0, 0, -1, 1, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0]])

    te=np.array([[0, 0, 1, 1, 1, 1, 0, 0],
                 [-1, 0, -1, 1, 1, 1, 0, 1],
                 [-1, -1, -1, -1, 1, 1, 1, 1],
                 [-1, 1, -1, -1, -1, 1, 1, 1],
                 [-1, 1, -1, -1, -1, 1, 1, 1],
                 [-1, -1, -1, -1, -1, -1, 1, 1],
                 [0, 0, -1, -1, -1, -1, 0, 0],
                 [0, -1, -1, -1, -1, -1, -1, 0]])

    te2=np.array([[0, 0, -1, 0, 1, 0, 0, 0],
                 [0, 0, -1, 1, 1, 1, 0, 0],
                 [-1, -1, -1, 1, -1, -1, 0, 0],
                 [0, 0, 1, -1, -1, -1, 0, 0],
                 [0, 0, -1, 1, -1, -1, 0, 0],
                 [0, 0, -1, -1, -1, -1, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0]])

    te3=np.array([[0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 1],
                 [0, 0, 0, -1, -1, -1, 0, 1],
                 [0, 0, 0, -1, -1, -1, -1, 1],
                 [0, 0, 0, -1, -1, -1, 1, 1],
                 [0, 0, 0, -1, -1, 1, 1, 1],
                 [0, 0, 1, 1, 1, 1, 1, 1],
                 [0, 1, 1, 1, 1, 1, 1, 1]])
    ai.go(te)
    print(ai.candidate_list)
    # print(ai.is_sb(te2, 1, (6, 0)))
    # print(ai.count_stable(te, 1))