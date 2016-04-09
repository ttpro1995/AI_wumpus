# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
from agents import Direction

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """
    #this is a interface for write code below

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


FORWARD = "Forward"
TURN_LEFT = "TurnLeft"
TURN_RIGHT = "TurnRight"

class RouteProblem(SearchProblem):
    """
    Search problem for Wumpus
    """

    def __init__(self, start, goal, allowed):
        '''
        successors ( ((x,y),direction), action, cost  )

        state :  ((x,y),direction))

        action-set = [TurnRight, TurnLeft, Forward]

        :param start:((x,y),direction),
        (x,y): the real position of agent where it need to search route
        direction: real direction of agent
        :param goal: set of goal positions
        :param allowed: an array of position (x,y) whether the agent is allowed to cross
        '''

        self.start = start
        self.goal = goal
        self.allowed = allowed

    def getStartState(self):
        '''
        :return start state (from input):
        '''
        return self.start

    def isGoalState(self, state):
        '''
        check whether state is goal state
        :param state: position (x,y)
        :return: True if (x,y) is desire destination
        '''
        position = state[0]
        for p in self.goal:
            if position == p:
                return True
        return False

    def getSuccessors(self, state):
        '''
        :param state: ((x,y),direction)
        :return: an array of successor (nextState, action, cost)
        '''

        cost = 1
        succ = []

        position = state[0]
        direction = state[1]

        cur_x = position[0]
        cur_y = position[1]

        right_p = (cur_x+1, cur_y)
        left_p = (cur_x-1, cur_y)
        down_p = (cur_x, cur_y+1)
        up_p = (cur_x,cur_y-1)

        if direction is Direction.R:
            if right_p in self.allowed:
                nextState = (right_p,Direction.R)
                action = FORWARD
                succ.append((nextState,action,cost))

            if up_p in self.allowed:
                nextState = (position,Direction.U)
                action = TURN_LEFT
                succ.append((nextState, action, cost))

            if down_p in self.allowed or left_p in self.allowed : # turn right if right or behind is allow
                nextState = (position,Direction.D)
                action = TURN_RIGHT
                succ.append((nextState, action, cost))



        if direction is Direction.L:
            if left_p in self.allowed:
                nextState = (left_p, Direction.L)
                action = FORWARD
                succ.append((nextState, action, cost))

            if down_p in self.allowed:
                nextState = (position, Direction.D)
                action = TURN_LEFT
                succ.append((nextState, action, cost))

            if up_p in self.allowed or right_p in self.allowed:
                nextState = (position, Direction.U)
                action = TURN_RIGHT
                succ.append((nextState, action, cost))

        if direction is Direction.U:
            if up_p in self.allowed:
                nextState = (up_p, Direction.U)
                action = FORWARD
                succ.append((nextState, action, cost))

            if left_p in self.allowed:
                nextState = (position, Direction.L)
                action = TURN_LEFT
                succ.append((nextState, action, cost))

            if right_p in self.allowed or down_p in self.allowed:
                nextState = (position, Direction.R)
                action = TURN_RIGHT
                succ.append((nextState, action, cost))

        if direction is Direction.D:
            if down_p in self.allowed:
                nextState = (down_p, Direction.D)
                action = FORWARD
                succ.append((nextState, action, cost))

            if right_p in self.allowed:
                nextState = (position, Direction.R)
                action = TURN_LEFT
                succ.append((nextState, action, cost))

            if left_p in self.allowed or up_p in self.allowed:
                nextState = (position, Direction.L)
                action = TURN_RIGHT
                succ.append((nextState, action, cost))

        return succ




    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        pass


def depthFirstSearch(problem):
    #problem is class SearchsProblem or PositionSearchProblem in searchsAgent.py

    
    if problem.isGoalState(problem.getStartState()):
        return []
    
    fringe = util.Stack()
    fringe.push(problem.getStartState())
    expored = set({})
    tb = util.TraceBack(problem.getStartState())
    
    while not fringe.isEmpty():
        node = fringe.pop()
        expored.add(node)
        if problem.isGoalState(node): 
            return tb.trace(node)
        for (successor, action, stepCost) in problem.getSuccessors(node):
            if not(successor in expored): #and not(successor in fringe.list):
                tb.push(node, action, successor)
                fringe.push(successor)
    return None

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""

    
    
    if problem.isGoalState(problem.getStartState()):
        return []
    
    fringe = util.Queue()
    fringe.push(problem.getStartState())
    expored = set({})
    tb = util.TraceBack(problem.getStartState())
    while True:
        if fringe.isEmpty():
            return None
        node = fringe.pop()
        expored.add(node)
        if problem.isGoalState(node): 
            return tb.trace(node)
        for (successor, action, stepCost) in problem.getSuccessors(node):
            if not(successor in expored) and not(successor in fringe.list):
                tb.push(node, action, successor)
                fringe.push(successor)

def uniformCostSearch(problem):
    """Search the node of least total cost first."""

    
    start = problem.getStartState()
    if problem.isGoalState(start):
        return []
    g = {}
    g[start] = 0
    fringe = util.PriorityQueue()
    fringe.push(start, g[start])
    expored = set({})
    tb = util.TraceBack(start)
    while not fringe.isEmpty():
        node = fringe.pop()
        expored.add(node)
        if problem.isGoalState(node): 
            return tb.trace(node)
        
        h = problem.getSuccessors(node)
        for (successor, action, stepCost) in h:
            isInFringe = any(successor in x for x in fringe.heap)
            if not(successor in expored) and not isInFringe:
                tb.push(node, action, successor)
                g[successor] = g[node] + stepCost
                fringe.push(successor, g[successor])
        
            if isInFringe:
                if g[successor] > g[node] + stepCost:
                    g[successor] = g[node] + stepCost
                    fringe.push(successor, g[successor]) #true some how
                    tb.push(node, action, successor)
                    if successor in expored:
                        expored.remove (successor) 
    return None

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    if problem.isGoalState(problem.getStartState()):
        return []
    
    fringe = util.PriorityQueue()
    start = problem.getStartState()
    fringe.push(start, heuristic(start, problem))
    expored = set({})
    tb = util.TraceBack(start)
    g = {}
    f = {}
    g[start] = 0
    f[start] = heuristic(start, problem)
    
    while not fringe.isEmpty():
        node = fringe.pop()
        expored.add(node)
        if problem.isGoalState(node): return tb.trace(node)
        for (successor, action, stepCost) in problem.getSuccessors(node):
            h_succ = heuristic(successor, problem)
            isInFringe = any (successor in x for x in fringe.heap)
            if not(successor in expored) and not isInFringe or (isInFringe and g[successor] > g[node] + stepCost):
                tb.push(node, action, successor)
                g[successor] = g[node] + stepCost
                f[successor] = g[successor] + h_succ
                fringe.push(successor,f[successor])
                if successor in expored: expored.remove (successor) 
    return None

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch


def plan_route(current,goal,allowed):
    problem = RouteProblem(current,goal,allowed)
    return aStarSearch(problem)