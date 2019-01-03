# valueIterationAgents.py
# -----------------------
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


import mdp, util

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0 # Utility

        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        states = mdp.getStates()

        for i in range(0,self.iterations):
            oldValues = self.values.copy()
            for state in states:
                if mdp.isTerminal(state) == 0:
                    maxUtility = []
                    for action in mdp.getPossibleActions(state):
                        sumUtility = 0.0
                        for nextstate, prob in mdp.getTransitionStatesAndProbs(state, action):
                            Us_prim = oldValues[nextstate]
                            sumUtility += mdp.getReward(state, action, nextstate)+ prob * (self.discount * Us_prim)
                        maxUtility.append(sumUtility)

                    self.values[state] = max(maxUtility)
                else:
                    self.values[state] = 0





    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        qValue = 0
        for nextstate, prob in self.mdp.getTransitionStatesAndProbs(state, action):
            qValue += self.mdp.getReward(state, action, nextstate) + prob * (self.discount * self.values[nextstate])


        return qValue

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        bestAction = ""
        value = -float("inf")
        for action in self.mdp.getPossibleActions(state):
            if value < self.computeQValueFromValues(state,action):
                value = self.computeQValueFromValues(state,action)
                bestAction = action

        if state == "TERMINAL_STATE": return None
        return bestAction

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
