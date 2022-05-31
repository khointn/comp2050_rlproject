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
import collections

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
        self.values = util.Counter() # A Counter is a dict with default 0
        self.runValueIteration()

    def runValueIteration(self):
        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        for _ in range(self.iterations):
            newValues = self.values.copy()

            # get Q_values for each possible s_prime
            for state in self.mdp.getStates():
                Q_values = [float('-inf')]

                # Terminal states have 0 value.
                if self.mdp.isTerminal(state):
                    newValues[state] = 0
                else:
                    legalActions = self.mdp.getPossibleActions(state)
                    for action in legalActions:
                        Q_values.append(self.getQValue(state, action))

                    # update value function at state s to largest Q_value
                    newValues[state] = max(Q_values)
            self.values = newValues

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
        possibleStates = self.mdp.getTransitionStatesAndProbs(state, action)
        sumQVal = 0

        for s, p in possibleStates:
            sumQVal += p * (self.mdp.getReward(state, action, s) + self.discount*self.getValue(s)) # formula here : https://inst.eecs.berkeley.edu/~cs188/fa18/assets/notes/n4.pdf

        return sumQVal
        util.raiseNotDefined()

    def computeActionFromValues(self, state):
        """
            The policy is the best action in the given state
            according to the values currently stored in self.values.

            You may break ties any way you see fit.  Note that if
            there are no legal actions, which is the case at the
            terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        actions = self.mdp.getPossibleActions(state)
        if len(actions) == 0:
            return None

        maxQ, maxA = -float('inf'), actions[0]
        for a in actions:
            tmpQ = self.getQValue(state, a)
            if tmpQ > maxQ:
                maxQ, maxA = tmpQ, a
        return maxA

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)

class AsynchronousValueIterationAgent(ValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        An AsynchronousValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs cyclic value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 1000):
        """
          Your cyclic value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy. Each iteration
          updates the value of only one state, which cycles through
          the states list. If the chosen state is terminal, nothing
          happens in that iteration.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state)
              mdp.isTerminal(state)
        """
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        possibleStates = self.mdp.getStates()
        for state in range(self.iterations):
                newValues = self.values.copy()
                # get Q_values for each possible s_prime
                Qvalues = [float('-inf')]

                # Terminal states have 0 value.
                if self.mdp.isTerminal(possibleStates[state % len(possibleStates)]):
                    newValues[possibleStates[state % len(possibleStates)]] = 0
                else:
                    legalActions = self.mdp.getPossibleActions(possibleStates[state % len(possibleStates)])

                    for action in legalActions:
                        Qvalues.append(self.getQValue(possibleStates[state % len(possibleStates)], action))

                    # update value function at state s to largest Q_value
                    newValues[possibleStates[state % len(possibleStates)]] = max(Qvalues)

                self.values = newValues

class PrioritizedSweepingValueIterationAgent(AsynchronousValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A PrioritizedSweepingValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs prioritized sweeping value iteration
        for a given number of iterations using the supplied parameters.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100, theta = 1e-5):
        """
          Your prioritized sweeping value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy.
        """
        self.theta = theta
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"

        count = 0

        states = self.mdp.getStates()
        adjMatrix = []
        state_to_index = util.Counter()

        for s_i in states:
            adj_list = set()

            for s_j in states:
                actions = self.mdp.getPossibleActions(s_j)

                for action in actions:
                    state_prob = self.mdp.getTransitionStatesAndProbs(s_j, action)

                    for new_state, prob in state_prob:
                        if new_state == s_i and prob > 0:
                            adj_list.add(s_j)

            adjMatrix.append(adj_list)
            state_to_index[s_i] = count
            count += 1

        # initialize a priority queue
        p_queue = util.PriorityQueue()
        new_values = util.Counter()
        # find diff of each s, store new value in new_values, push s, -diff
        for state in states:
            actions = self.mdp.getPossibleActions(state)
            if self.mdp.isTerminal(state):
                continue
            current_value = self.getValue(state)
            best_action = self.computeActionFromValues(state)
            
            if best_action:
                new_value = self.computeQValueFromValues(state, best_action)
                new_values[state] = new_value
                diff = abs(current_value - new_value)
                p_queue.push(state, -diff)
            else:
                new_values[state] = current_value

        # do iterations
        for _ in range(self.iterations):
            # if p_queue is empty, terminate
            if p_queue.isEmpty():
                break
            front = p_queue.pop()
            if not self.mdp.isTerminal(front):
                self.values[front] = new_values[front]
            # precess front's pred
            for pred in adjMatrix[state_to_index[front]]:
                current_value = self.getValue(pred)
                best_action = self.computeActionFromValues(pred)
                if best_action:
                    new_value = self.computeQValueFromValues(pred, best_action)
                    diff = abs(current_value - new_value)
                    new_values[pred] = new_value
                    if diff > self.theta:
                        p_queue.update(pred, -diff)

