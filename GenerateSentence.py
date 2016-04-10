from collections import defaultdict
from logic import *

def pp(l):
    for i in l:
        print(i)

#No Wumpus or Pit at location 1,1
#def axiom_generator_initial_location_assertions(x, y):
def genInitSafeLoctionLogic(xInit,yInit):
    WumpusInit = Expr("W{}_{}".format(xInit,yInit))
    PitInit = Expr("P{}_{}".format(xInit,yInit))
    return ~(WumpusInit | PitInit)


def genPerceptToKnowLedgeSentence(timecounter, mapsize):
    l = []
    for i in range(1, mapsize+1):
        for j in range(1, mapsize+1):
            L_xyt = Expr("L{}_{}_{}".format(i, j, timecounter))
            Breeze_t = Expr("Breeze{}".format(timecounter))
            B_xy = Expr("B{}_{}".format(i, j))
            sentence = Expr(L_xyt >> (Breeze_t % B_xy))
            l.append(sentence)
            Stench_t = Expr("Stench{}".format(timecounter))
            W_xy = Expr("B{}_{}".format(i, j))
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


def genActionAffectLogic(t, mapsize):
    l = []
    def genMoveActionLogic(x,y):
        Lcur = Expr("L{}_{}_{}".format(x,y,t))
        Forward = Expr("Forward{}".format(t))
        if x - 1 >= 1:
            FacingNorth = Expr("FacingNorth{}".format(t))
            Lmove = Expr("L{}_{}_{}".format(x-1,y,t+1))
            Lchance = Expr("~L{}_{}_{}".format(x,y,t+1))
            l.append((Lcur & FacingNorth & Forward) >> (Lmove & Lchance))
        if x + 1 <= mapsize:
            FacingSouth = Expr("FacingSouth{}".format(t))
            Lmove = Expr("L{}_{}_{}".format(x+1,y,t+1))
            Lchance = Expr("~L{}_{}_{}".format(x,y,t+1))
            l.append((Lcur & FacingSouth & Forward) >> (Lmove & Lchance))
        if y - 1 >= 1:
            FacingEast = Expr("FacingEast{}".format(t))
            Lmove = Expr("L{}_{}_{}".format(x,y-1,t+1))
            Lchance = Expr("~L{}_{}_{}".format(x,y,t+1))
            l.append((Lcur & FacingEast & Forward) >> (Lmove & Lchance))
        if y + 1 <= mapsize:
            FacingWest = Expr("FacingWest{}".format(t))
            Lmove = Expr("L{}_{}_{}".format(x,y+1,t+1))
            Lchance = Expr("~L{}_{}_{}".format(x,y,t+1))
            l.append((Lcur & FacingWest & Forward) >> (Lmove & Lchance))

    def genTurnActionLogic():
        FacingNorthCur = Expr("FacingNorth{}".format(t))
        FacingNorthTurn = Expr("FacingNorth{}".format(t+1))
        FacingNorthChange = Expr("~FacingNorth{}".format(t+1))
        FacingSouthCur = Expr("FacingSouth{}".format(t))
        FacingSouthTurn = Expr("FacingSouth{}".format(t+1))
        FacingSouthChange = Expr("~FacingSouth{}".format(t+1))
        FacingEastCur = Expr("FacingEast{}".format(t))
        FacingEastTurn = Expr("FacingEast{}".format(t+1))
        FacingEastChange = Expr("~FacingEast{}".format(t+1))
        FacingWestCur = Expr("FacingWest{}".format(t))
        FacingWestTurn = Expr("FacingWest{}".format(t+1))
        FacingWestChange = Expr("~FacingWest{}".format(t+1))
        TurnLeft = Expr("TurnLeft{}".format(t))
        TurnRight = Expr("TurnRight".format(t))
        l.append((FacingNorthCur & TurnRight) >> (FacingEastTurn & FacingNorthChange))
        l.append((FacingNorthCur & TurnLeft) >> (FacingWestTurn & FacingNorthChange))
        l.append((FacingSouthCur & TurnRight) >> (FacingWestTurn & FacingSouthChange))
        l.append((FacingSouthCur & TurnLeft) >> (FacingEastTurn & FacingSouthChange))
        l.append((FacingEastCur & TurnRight) >> (FacingSouthTurn & FacingEastChange))
        l.append((FacingEastCur & TurnLeft) >> (FacingNorthTurn & FacingEastChange))
        l.append((FacingWestCur & TurnRight) >> (FacingNorthTurn & FacingWestChange))
        l.append((FacingWestCur & TurnLeft) >> (FacingSouthTurn & FacingWestChange))

    Shoot  = "Shoot{}".format(t)
    HaveArrow =  "HaveArrow".format(t)
    genTurnActionLogic()
    for i in range(1, mapsize+1):
        for j in range(1, mapsize+1):
            genMoveActionLogic(i,j)
    return l

#pp(genActionAffectLogic(1,3))

#agent only at one location at a time
def genOnlyOneLoctionAtTime(xcur, ycur, mapsize, t = 0):
    l = None
    location = "L{}_{}_{} >>".format(xcur,ycur,t)
    notLocation = []
    for i in range(1, mapsize+1):
        for j in range(1, mapsize+1):
            if i == xcur and j == ycur:
                pass
            else:
                notLocation.append(" ~L{}_{}_{}".format(i,j,t))
    l = expr(location + "(" + "&".join(notLocation) + ")")
    return l

#print(genOnlyOneLoctionAtTime(1,2,3,0))

def genOnlyOneHeadingAtTime(heading, t = 0):
    axiom_str = ''
    headingList = ['North', 'South', 'East', 'West']
    notHeading = []
    for h in headingList:
        if h.upper() == heading.upper():
            axiom_str += 'Heading' + h + str(t)
        else:
            notHeading.append('~Heading' + h + str(t))
    axiom_str += ' >> ('
    axiom_str += ' & '.join(notHeading)
    axiom_str += ')'

    return axiom_str

#print(genOnlyOneHeadingAtTime("North",0))

def genHaveArrowAndWumpusAlive(t = 0):
    """
    Assert that Agent has the arrow and the Wumpus is alive at time t.

    t := time; default=0
    """
    return "HaveArrow{}".format(t) + ' & ' + "WumpusAlive{}".format(t)


def initial_wumpus_axioms(xInit, yInit, mapsize, heading):
    """
    Generate all of the initial wumpus axioms

    xi,yi = initial location
    width,height = dimensions of world
    heading = str representation of the initial agent heading
    """
    sentence = [genInitSafeLoctionLogic(xInit,yInit)]
    sentence.extend(genOneWumpusExistLogic(mapsize))
    sentence.extend(genBreezeStenchLogic(mapsize))
    sentence.extend(genHaveArrowAndWumpusAlive(0))

    sentence.extend(genOnlyOneLoctionAtTime(xInit,yInit,mapsize,0))
    sentence.extend(genOnlyOneHeadingAtTime(heading,0))
    return sentence


#-------------------------------------------------------------------------------
# Axiom Generators: Temporal Axioms (added at each time step)
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# Transition model: Successor-State Axioms (SSA's)
# Avoid the frame problem(s): don't write axioms about actions, write axioms about
# fluents!  That is, write successor-state axioms as opposed to effect and frame
# axioms
#
# The general successor-state axioms pattern (where F is a fluent):
#   F^{t+1} <=> (Action(s)ThatCause_F^t) | (F^t & ~Action(s)ThatCauseNot_F^t)

# NOTE: this is very expensive in terms of generating many (~170 per axiom) CNF clauses!
def axiom_generator_at_location_ssa( x, y,mapsize, t):
    """
    Assert the condidtions at time t under which the agent is in
    a particular location (state_loc_str: L) at time t+1, following
    the successor-state axiom pattern.

    See Section 7. of AIMA.  However...
    NOTE: the book's version of this class of axioms is not complete
          for the version in Project 3.

    x,y := location
    t := time
    mapsize := the bounds of the environment.
    """
    axiom_str = ''
    axiom_str += "L{}_{}_{}".format(x,y,t) + " % ("

    succ_locations = []
    for xs in range(x-1, x+2):
        for ys in range(y-1, y+2):
            if xs >= 1 and xs <= mapsize and ys >= 1 and ys <= mapsize:
                succ_locations.append("L{}_{}_{}".format(xs,ys,t+1))

    axiom_str += " | ".join(succ_locations)
    axiom_str += ")"

    return axiom_str

def generate_at_location_ssa(t, x, y, mapsize, heading):
    """
    The full at_location SSA converts to a fairly large CNF, which in
    turn causes the KB to grow very fast, slowing overall inference.
    We therefore need to restric generating these axioms as much as possible.
    This fn generates the at_location SSA only for the current location and
    the location the agent is currently facing (in case the agent moves
    forward on the next turn).
    This is sufficient for tracking the current location, which will be the
    single L location that evaluates to True; however, the other locations
    may be False or Unknown.
    """
    axioms = [axiom_generator_at_location_ssa( x, y, mapsize, t)]
    if heading == 'west' and x - 1 >= 1:
        axioms.append(axiom_generator_at_location_ssa(t, x-1, y, mapsize))
    if heading == 'east' and x + 1 <= mapsize:
        axioms.append(axiom_generator_at_location_ssa(t, x+1, y, mapsize))
    if heading == 'south' and y - 1 >= 1:
        axioms.append(axiom_generator_at_location_ssa(t, x, y-1, mapsize))
    if heading == 'north' and y + 1 <= mapsize:
        axioms.append(axiom_generator_at_location_ssa(t, x, y+1, mapsize))
    if len(axioms) == 0:
        print('axiom_generator_at_location_ssa')
    return filter(lambda s: s != '', axioms)

#----------------------------------

def axiom_generator_have_arrow_ssa(t):
    """
    Assert the conditions at time t under which the Agent
    has the arrow at time t+1

    t := time
    """
    return "HaveArror{}".format(t+1) +  " % (" + "HaveArrow{}".format(t) +\
           " & ~" + "Shoot{}".format(t) + ")"

def axiom_generator_wumpus_alive_ssa(t):
    """
    Assert the conditions at time t under which the Wumpus
    is known to be alive at time t+1

    (NOTE: If this axiom is implemented in the standard way, it is expected
    that it will take one time step after the Wumpus dies before the Agent
    can infer that the Wumpus is actually dead.)

    t := time
    """
    return  "WumpusAlive".format(t+1) + " % (" + "WumpusAlive".format(t) +\
            " & ~" + "Screem{}".format(t+1)

#----------------------------------


def axiom_generator_heading_north_ssa(t):
    """
    Assert the conditions at time t under which the
    Agent heading will be North at time t+1

    t := time
    """
    axiom_str = ''
    axiom_str += "FacingNorth{}".format(t+1) + " % ((" + "FacingNorth{}"(t) + " & ~"\
                 + "TurnRight{}".format(t) + " & ~" + "TurnLeft{}".format(t) + ") | "
    axiom_str += "FacingEast{}".format(t) + " & " + "TurnLeft{}".format(t) + ") | "
    axiom_str += "FacingWest{}".format(t) + " & " + "TurnRight{}".format(t) + "))"
    # Comment or delete the next line once this function has been implemented.
    # utils.print_not_implemented()
    return axiom_str

def axiom_generator_heading_east_ssa(t):
    """
    Assert the conditions at time t under which the
    Agent heading will be East at time t+1

    t := time
    """
    axiom_str = ''
    axiom_str += "FacingEast{}".format(t+1) + " % ((" + "FacingEast{}".format(t) + " & ~"\
                 + "TurnRight{}".format(t) + " & ~" + "TurnLeft{}".format(t) + ") | "
    axiom_str += "FacingSouth{}".format(t) + " & " + "TurnLeft{}".format(t) + ") | "
    axiom_str += "FacingNorth{}".format(t) + " & " + "TurnRight{}".format(t) + "))"
    return axiom_str

def axiom_generator_heading_south_ssa(t):
    """
    Assert the conditions at time t under which the
    Agent heading will be South at time t+1

    t := time
    """
    axiom_str = ''
    axiom_str += "FacingSouth{}".format(t+1) + " % ((" + "FacingSouth{}".format(t) + " & ~"\
                 + "TurnRight{}".format(t) + " & ~" + "TurnLeft{}".format(t) + ") | "
    axiom_str += "FacingWest{}".format(t) + " & " + "TurnLeft{}".format(t) + ") | "
    axiom_str += "FacingEast{}".format(t) + " & " + "TurnRight{}".format(t) + "))"
    return axiom_str

def axiom_generator_heading_west_ssa(t):
    """
    Assert the conditions at time t under which the
    Agent heading will be West at time t+1

    t := time
    """
    axiom_str = ''
    axiom_str += "FacingWest{}".format(t+1) + " % ((" + "FacingWest{}".format(t) + " & ~"\
                 + "TurnRight{}".format(t) + " & ~" + "TurnLeft{}".format(t) + ") | "
    axiom_str += "FacingNorth{}".format(t) + " & " + "TurnLeft{}".format(t) + ") | "
    axiom_str += "FacingSouth{}".format(t) + " & " + "TurnRight{}".format(t) + "))"
    return axiom_str

def generate_heading_ssa(t):
    """
    Generates all of the heading SSAs.
    """
    return [axiom_generator_heading_north_ssa(t),
            axiom_generator_heading_east_ssa(t),
            axiom_generator_heading_south_ssa(t),
            axiom_generator_heading_west_ssa(t)]

def generate_non_location_ssa(t):
    """
    Generate all non-location-based SSAs
    """
    axioms = [] # all_state_loc_ssa(t, xmin, xmax, ymin, ymax)
    axioms.append(axiom_generator_have_arrow_ssa(t))
    axioms.append(axiom_generator_wumpus_alive_ssa(t))
    axioms.extend(generate_heading_ssa(t))
    return filter(lambda s: s != '', axioms)

#----------------------------------

def axiom_generator_heading_only_north(t):
    """
    Assert that when heading is North, the agent is
    not heading any other direction.

    t := time
    """
    return genOnlyOneHeadingAtTime("north", t)

def axiom_generator_heading_only_east(t):
    """
    Assert that when heading is East, the agent is
    not heading any other direction.

    t := time
    """
    return genOnlyOneHeadingAtTime("east", t)

def axiom_generator_heading_only_south(t):
    """
    Assert that when heading is South, the agent is
    not heading any other direction.

    t := time
    """
    return genOnlyOneHeadingAtTime("south", t)

def axiom_generator_heading_only_west(t):
    """
    Assert that when heading is West, the agent is
    not heading any other direction.

    t := time
    """
    return genOnlyOneHeadingAtTime("west", t)

def generate_heading_only_one_direction_axioms(t):
    return [axiom_generator_heading_only_north(t),
            axiom_generator_heading_only_east(t),
            axiom_generator_heading_only_south(t),
            axiom_generator_heading_only_west(t)]


def axiom_generator_only_one_action_axioms(t):
    """
    Assert that only one axion can be executed at a time.

    t := time
    """
    axiom_str = ''
    axiom_str_arr= ["Forward{}".format(t), "Grab{}".format(t), "Shoot{}".format(t),
                    "Climb{}".format(t), "TurnLeft{}".format(t), "TurnRight{}".format(t), "Wait{}".format(t)]
    axioms = []
    for i in range(0, len(axiom_str_arr)):
        for j in range(i+1, len(axiom_str_arr)):
            axioms.append("(~" + axiom_str_arr[i] + "|~" + axiom_str_arr[j] + ")")

    axiom_str = "("+ '|'.join(axiom_str_arr) + ")&"
    axiom_str += "(" + ' & '.join(axioms) + ")"
    return axiom_str


def generate_mutually_exclusive_axioms(t):
    """
    Generate all time-based mutually exclusive axioms.
    """
    axioms = []

    # must be t+1 to constrain which direction could be heading _next_
    axioms.extend(generate_heading_only_one_direction_axioms(t + 1))

    # actions occur in current time, after percept
    axioms.append(axiom_generator_only_one_action_axioms(t))

    return filter(lambda s: s != '', axioms)

#------------------------------------------------------------------
