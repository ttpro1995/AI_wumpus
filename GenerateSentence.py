from collections import defaultdict
from logic import *


def genPerceptToKnowLedgeSentence(timecounter, mapsize):
    l = []
    for i in range(1, mapsize+1):
        for j in range(1, mapsize+1):
            L_xyt = Expr("L{}_{}_{}".format(i, j, timecounter))
            Breeze_t = Expr("Breeze{}".format(timecounter))
            B_xy = Expr("B{}_{}".format(i, j))
            sentence = Expr(L_xyt >> (Breeze_t % B_xy))
            l.append(sentence)
    return l

#test for timecounter = 3, mapsize = 4
#print(genPerceptToKnowLedgeSentence(3,4))
# L113 >> (Breeze3 % B11)
# L123 >> (Breeze3 % B12)
# L133 >> (Breeze3 % B13)
# L143 >> (Breeze3 % B14)
# L213 >> (Breeze3 % B21)
# L223 >> (Breeze3 % B22)
# L233 >> (Breeze3 % B23)
# L243 >> (Breeze3 % B24)
# L313 >> (Breeze3 % B31)
# L323 >> (Breeze3 % B32)
# L333 >> (Breeze3 % B33)
# L343 >> (Breeze3 % B34)
# L413 >> (Breeze3 % B41)
# L423 >> (Breeze3 % B42)
# L433 >> (Breeze3 % B43)
# L443 >> (Breeze3 % B44)


def genBreezeStenchLogic(mapsize):
    """
    B11 % (P12 | P21)
    S11 % (W12 | W21)
    """

    l = []
    for i in range(1, mapsize+1):
        for j in range(1, mapsize+1):
            listHypoSquarePit = []
            listHypoSquareWumpus = []
            list_Pit_expr = []
            list_Wumpus_expr = []
            if i - 1 >= 1:
                listHypoSquarePit.append("P{}_{}".format(i-1, j))
                listHypoSquareWumpus.append("W{}_{}".format(i-1, j))
            if i + 1 <= mapsize:
                listHypoSquarePit.append("P{}_{}".format(i+1, j))
                listHypoSquareWumpus.append("W{}_{}".format(i+1, j))
            if j - 1 >= 1:
                listHypoSquarePit.append("P{}_{}".format(i, j-1))
                listHypoSquareWumpus.append("W{}_{}".format(i, j-1))
            if j + 1 <= mapsize:
                listHypoSquarePit.append("P{}_{}".format(i, j+1))
                listHypoSquareWumpus.append("W{}_{}".format(i, j+1))

            # Turn String into Expr
            for pit_str in listHypoSquarePit:
                pit_expr = Expr(pit_str)
                list_Pit_expr.append(pit_expr)
            for wumpus_str in listHypoSquareWumpus:
                wumpus_expr = Expr(wumpus_str)
                list_Wumpus_expr.append(wumpus_expr)

            B_xy = Expr("B{}_{}".format(i, j))
            S_xy = Expr("S{}_{}".format(i, j))


            if (list_Pit_expr):
                dis_expr = list_Pit_expr[0]
                for e in list_Pit_expr: # disjuntion pit
                    dis_expr = Expr(dis_expr|e)
                sum_pit = B_xy % dis_expr
                l.append(sum_pit)  #  B11 % (P12 | P21 | ...)

            if (list_Wumpus_expr):
                dis_expr = list_Pit_expr[0]
                for e in list_Wumpus_expr:  # disjuntion wumpus
                    dis_expr = Expr(dis_expr | e)
                sum_wumpus = S_xy % dis_expr
                l.append(sum_wumpus)  # S11 % (W12 | W21 | ...)

            #  l.append("B{}_{}".format(i,j) + " % ( " + " | ".join(str(i) for i in listHypoSquarePit) + " )")
            #  l.append("S{}_{}".format(i,j) + " % ( " + " | ".join(str(i) for i in listHypoSquareWumpus) + " )")
    return l

#  test with world size = 3
#  print(genBreezeStenchLogic(3))


def genOneWumpusExistLogic(mapsize):
    l = []
    exist = []
    check = defaultdict(defaultdict)
    for i in range(1, mapsize+1):
        for j in range(1, mapsize+1):
            for n in range(1, mapsize+1):
                for m in range(1, mapsize+1):
                    check[(i, j)][(n, m)] = False

    for i in range(1, mapsize+1):
        for j in range(1, mapsize+1):
            W_xy = Expr("W{}_{}".format(i, j))
            exist.append(W_xy)
            # exist.append("W{}_{}".format(i,j))

            # not disjunction
            if i - 1 >= 1 and check[(i, j)][(i-1, j)] == False:
                A = ~Expr("W{}_{}".format(i, j))
                B = ~Expr("W{}_{}".format(i-1, j))
                disAB = Expr(A|B)
                l.append(disAB)
                # l.append("~W{}_{}".format(i,j) + " | " + "~W{}_{}".format(i-1,j))
                check[(i, j)][(i-1, j)] = True
                check[(i-1, j)][(i, j)] = True

            if i + 1 <= mapsize and check[(i, j)][(i+1, j)] == False:
                A = ~Expr("W{}_{}".format(i, j))
                B = ~Expr("W{}_{}".format(i+1, j))
                disAB = Expr(A|B)
                l.append(disAB)
                # l.append("~W{}_{}".format(i,j) + " | " + "~W{}_{}".format(i+1,j))
                check[(i, j)][(i+1, j)] = True
                check[(i+1, j)][(i, j)] = True

            if j - 1 >= 1 and check[(i, j)][(i, j-1)] == False:
                A = ~Expr("W{}_{}".format(i, j))
                B = ~Expr("W{}_{}".format(i, j-1))
                disAB = Expr(A | B)
                l.append(disAB)
                # l.append("~W{}_{}".format(i,j) + " | " + "~W{}_{}".format(i,j-1))
                check[(i,j)][(i,j-1)] = True
                check[(i,j-1)][(i,j)] = True

            if j + 1 <= mapsize and check[(i, j)][(i, j+1)] == False:
                A = ~Expr("W{}_{}".format(i, j))
                B = ~Expr("W{}_{}".format(i, j+1))
                disAB = Expr(A|B)
                l.append(disAB)
                #l.append("~W{}_{}".format(i,j) + " | " + "~W{}_{}".format(i,j+1))
                check[(i, j)][(i, j+1)] = True
                check[(i, j+1)][(i, j)] = True

    if exist: # Wxy | Wxy | Wxy ...
        dis_Wxy = exist[0]
        for e in exist:
            dis_Wxy = Expr(dis_Wxy|e)
        l.append(dis_Wxy)
    #l.append(" | ".join(str(i) for i in exist))
    return l

#test
#print(genOneWumpusExistLogic(6))

#OK_xyt % ~P_xy & ~(Wxy & WumpusAlive_t)
def genOKSquareLogic(timecounter, mapsize):
    l = []
    for i in range(1,mapsize+1):
        for j in range(1,mapsize+1):
            OK_xyt = Expr('OK{}_{}_{}'.format(i, j, timecounter))
            P_xy = Expr('~P{}_{}'.format(i, j))
            W_xy = Expr('W{}_{}'.format(i, j))
            WumpusAlive_t = Expr('WumpusAlive{}'.format(timecounter))
            sum = Expr(OK_xyt % ~P_xy & ~(W_xy & WumpusAlive_t))
            l.append(sum)
            # l.append("OK{}_{}_{} % (~P{}_{} & (W{}_{} & WumpusAlive{}))".format(i,j,timecounter,i,j,i,j,timecounter))
    return l
#test with world size = 6
#print(genOKSquareLogic(timecounter=5,mapsize=6))


