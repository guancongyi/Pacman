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

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

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

def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):

    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    """
    path = util.Stack()  # store result path successor
    visited = {}  # state and flag
    parent = {}  # succ and succ's parent

    rslt = []

    visited.update({problem.getStartState(): 1})
    currSucc = ((problem.getStartState(),None,None))
    path.push(currSucc)

    while (path.isEmpty() == 0):

        currState = currSucc[0]
        visited.update({currState:1})
        if problem.isGoalState(currState):
            rslt.append(currSucc)
            while parent.get(currSucc) != (problem.getStartState(),None,None):
                rslt.append(parent.get(currSucc))
                currSucc = parent.get(currSucc)
            break

        for square in problem.getSuccessors(currState):
            if visited.get(square[0]) == None:
                parent.update({square: currSucc})
                path.push(square)

        currSucc = path.pop()

    rslt.reverse()
    return [x[1] for x in rslt]

    #util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    path = util.Queue()  # store result path successor
    visited = {}  # state and flag
    parent = {}  # succ and succ's parent successor

    rslt = []  # succ

    currSucc = ((problem.getStartState(),None,None))
    path.push(currSucc)

    while path.isEmpty() == 0:
        currSucc = path.pop()
        visited.update({currSucc[0]: 1})
        # traceback
        if problem.isGoalState(currSucc[0]):
            rslt.append(currSucc)
            while parent.get(currSucc)[1] != None:
                rslt.append(parent.get(currSucc))
                currSucc = parent.get(currSucc)
            break

        for square in problem.getSuccessors(currSucc[0]):
            if visited.get(square[0]) == None:
                visited.update({square[0]:1})
                path.push(square)
                parent.update({square: currSucc})


    ret = [x[1] for x in rslt]

    ret.reverse()
    return ret

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    path = util.PriorityQueue()  # store result path successor
    visited = {}  # state and flag
    parent = {}  # succ and succ's parent successor
    cst = {}  # state and cumulative cost
    rslt = []  # succ

    currSucc = ((problem.getStartState(), None, 0))
    path.push(currSucc,currSucc[2])
    cst.update({currSucc[0]: 0})

    while path.isEmpty() == 0:
        currSucc = path.pop()
        currCost = cst.get(currSucc[0])
        visited.update({currSucc[0]: 1})

        if problem.isGoalState(currSucc[0]):
            rslt.append(currSucc)
            while parent.get(currSucc)[1] != None:
                rslt.append(parent.get(currSucc))
                currSucc = parent.get(currSucc)
            break

        for square in problem.getSuccessors(currSucc[0]):
            # not visited or neighbor's cost greater than current total cost
            if (visited.get(square[0]) == None) or (cst.get(square[0]) > currCost + square[2]):
                path.update(square, currCost + square[2])
                cst.update({square[0]: currCost + square[2]})
                parent.update({square: currSucc})
                visited.update({square[0]:1})

    ret = [x[1] for x in rslt]
    ret.reverse()
    return ret

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    #pq = util.PriorityQueue()
    path = util.PriorityQueue()  # store result path successor
    visited = {}  # state and flag
    parent = {}  # succ and succ's parent successor
    cst = {}  # state and cumulative cost

    rslt = []  # succ

    currSucc = (problem.getStartState(), None, 0)
    path.push(currSucc,0)
    cst.update({currSucc[0]: 0+heuristic(currSucc[0],problem)})

    while path.isEmpty() == 0:
        currSucc = path.pop()
        currCost = cst.get(currSucc[0])
        visited.update({currSucc[0]: 1})

        if problem.isGoalState(currSucc[0]):
            rslt.append(currSucc)
            while parent.get(currSucc)[1] != None:
                rslt.append(parent.get(currSucc))
                currSucc = parent.get(currSucc)
            break
        for square in problem.getSuccessors(currSucc[0]):
            gCost = currCost+square[2]
            hCost = heuristic(square[0],problem)
            fCost = gCost+hCost

            if visited.get(square[0]) == None or cst.get(square[0]) > gCost:
                parent.update({square: currSucc})
                visited.update({square[0]: 1})
                cst.update({square[0]: gCost})
                if cst.get(square[0]) > gCost:
                    path.update(square, fCost)
                else:
                    path.push(square, fCost)


    ret = [x[1] for x in rslt]
    ret.reverse()
    return ret


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
