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
            newValues = util.Counter()
            for state in self.mdp.getStates():
                temp = [sum([ns[1] * (self.mdp.getReward(state, a, ns[0]) + self.discount * self.values[ns[0]]) for ns in self.mdp.getTransitionStatesAndProbs(state, a)]) for a in self.mdp.getPossibleActions(state)]
                if len(temp) == 0 :
                    newValues[state] = 0
                else :
                    newValues[state] = max(temp)
            self.values = newValues.copy()


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
        return sum([ns[1] * (self.mdp.getReward(state, action, ns[0]) + self.discount * self.values[ns[0]]) for ns in self.mdp.getTransitionStatesAndProbs(state, action)])
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
        newValues = util.Counter()
        for _ in range(self.iterations):
            for a in self.mdp.getPossibleActions(state):
                newValues[a] = sum([ns[1] * (self.mdp.getReward(state, a, ns[0]) + self.discount * self.values[ns[0]]) for ns in self.mdp.getTransitionStatesAndProbs(state, a)])
        return newValues.argMax()
        util.raiseNotDefined()

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
        for i in range(self.iterations):
            state = self.mdp.getStates()[i % len(self.mdp.getStates())]
            if self.mdp.isTerminal(state) == False:
                self.values[state] = max([sum([ns[1] * (self.mdp.getReward(state, a, ns[0]) + self.discount * self.values[ns[0]]) for ns in self.mdp.getTransitionStatesAndProbs(state, a)]) for a in self.mdp.getPossibleActions(state)])

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
        predecessors = {state: [] for state in self.mdp.getStates()}
        for state in self.mdp.getStates():
            for action in self.mdp.getPossibleActions(state):
                for ns in self.mdp.getTransitionStatesAndProbs(state, action):
                    if (ns[1] != 0) and (state not in predecessors[ns[0]]):
                        predecessors[ns[0]].append(state)

        priorityQueue = util.PriorityQueue()
        for state in self.mdp.getStates():
            if self.mdp.isTerminal(state) == False:
                qValue = max([self.computeQValueFromValues(state, action) for action in self.mdp.getPossibleActions(state)])
                diff = abs(self.values[state] - qValue)
                priorityQueue.update(state, -diff)
        
        for _ in range(self.iterations):
            if not priorityQueue.isEmpty():
                s = priorityQueue.pop()
                self.values[s] = max([self.computeQValueFromValues(s, action) for action in self.mdp.getPossibleActions(s)])
                for p in predecessors[s]:
                    if self.mdp.isTerminal(p) == False:
                        qValue = max([self.computeQValueFromValues(p, action) for action in self.mdp.getPossibleActions(p)])
                        diff = abs(self.values[p] - qValue)
                        priorityQueue.update(p, -diff)
                    if diff > self.theta:
                        priorityQueue.update(p, -diff)


