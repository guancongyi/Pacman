# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        #newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        # choose an evaluation function to calculate a score for current state.
        # if ghost is far then 1/g_dist is small, - small value
        # if the distances to shortest food is close, then 1/f is large, + large value

        f_dist = []
        ret = successorGameState.getScore()

        g_dist = util.manhattanDistance(newGhostStates[0].getPosition(),newPos)
        if g_dist >0:
            ret -= 10/ g_dist


        for food in newFood.asList():
            f_dist.append(util.manhattanDistance(food,newPos))

        if len(f_dist) != 0:
            ret += 10/min(f_dist)

        return ret


def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)



class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        def minimax(state, depth, agent, totalagents):
            agent = agent%totalagents
            maxlist = []
            minlist = []

            if state.isWin() or state.isLose() or depth == self.depth*totalagents or state.getLegalActions(agent) == 0:
                return self.evaluationFunction(state)

            if agent == 0:
                for action0 in state.getLegalActions(agent):
                    maxlist.append(minimax(state.generateSuccessor(agent, action0), depth+1,agent+1,totalagents))
                return max(maxlist)

            else:
                for action in state.getLegalActions(agent):
                    minlist.append(minimax(state.generateSuccessor(agent,action),depth+1,agent+1,totalagents))
                return min(minlist)

        depth = 0
        maxlist = []
        totalagents = gameState.getNumAgents()
        for action in gameState.getLegalActions(0):
           maxlist.append((minimax(gameState.generateSuccessor(0, action), depth+1, 1, totalagents),action))


        return max(maxlist, key=lambda x: x[0])[1]



class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def alpha_beta(state, depth, agent, totalagents, alpha, beta):

            agent = agent % totalagents

            # if it is a leaf node
            if state.isWin() or state.isLose() or depth == self.depth*totalagents or state.getLegalActions(agent) == 0:
                return self.evaluationFunction(state)

            # if it is maximizer
            if agent == 0:
                bestval = -float("inf")
                for a0 in state.getLegalActions(0):
                    value = alpha_beta(state.generateSuccessor(0,a0),depth+1,agent+1,totalagents,alpha,beta)
                    bestval = max(bestval,value)
                    alpha = max(bestval,alpha)
                    if beta<alpha:
                        break
                return bestval

            else:
                bestval = float("inf")
                for a1 in state.getLegalActions(agent):
                    value = alpha_beta(state.generateSuccessor(agent,a1),depth+1,agent+1, totalagents, alpha, beta)
                    bestval = min(bestval,value)
                    beta = min(beta,bestval)
                    if beta < alpha:
                        break

                return bestval


        beta = float("inf")
        alpha = -beta
        score = alpha
        bestact = ""
        for action in gameState.getLegalActions(0):
            prevscore = score

            score = max(score, alpha_beta(gameState.generateSuccessor(0,action),1,1,gameState.getNumAgents(),alpha,beta))
            if score > prevscore:
                bestact = action

            if score > beta:
                return bestact

            alpha = max(alpha, score)

        return bestact


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        def expectimax(state, depth, agent, totalagents):
            agent = agent % totalagents
            if state.isWin() or state.isLose() or depth == self.depth*totalagents or state.getLegalActions(agent) == 0:
                return self.evaluationFunction(state)

            if agent == 0:
                value = -float("inf")
                templist = state.getLegalActions(agent)
                for action in templist:
                    value = max(value, expectimax(state.generateSuccessor(agent,action),depth+1,agent+1,totalagents))
                return value
            else:
                value = 0
                p = 0
                templist = state.getLegalActions(agent)
                for action in templist:
                    p = (float(1)/len(templist))
                    value += p * float(expectimax(state.generateSuccessor(agent,action),depth+1,agent+1,totalagents))
                return value


        depth = 0
        maxlist = []
        totalagents = gameState.getNumAgents()
        actionlist = gameState.getLegalActions(0)

        for action in actionlist:
            maxlist.append((expectimax(gameState.generateSuccessor(0,action),depth+1,1,totalagents),action))

        return max(maxlist, key=lambda x: x[0])[1]

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    pacman = currentGameState.getPacmanPosition()

    ghostDist = [util.manhattanDistance(ghost, pacman) for ghost in currentGameState.getGhostPositions()]
    closeGhostDist = 1.0 / (min(ghostDist) if min(ghostDist) != 0 else 1)

    score = currentGameState.getScore()

    numCapEaten = 1.0 / (len(currentGameState.getCapsules()) + 1)

    return closeGhostDist * 100 + score + numCapEaten * 1000


# Abbreviation
better = betterEvaluationFunction

