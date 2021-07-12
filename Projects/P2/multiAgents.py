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
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
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
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        dist = 0
        score = 0
        maxDist = 0
        if len(newFood.asList()) != 0:
            foodDist = [manhattanDistance(newPos, food) for food in newFood.asList()]
            dist = min(foodDist)
            maxDist = max(foodDist)
        ghostPos = [ghost.getPosition() for ghost in newGhostStates]
        danger = manhattanDistance(newPos, ghostPos[0])
        for ghost in ghostPos:
            if manhattanDistance(newPos, ghost) < danger:
                danger = manhattanDistance(newPos, ghost)
        score = successorGameState.getScore() + 0.1 * danger - 0.2 * dist
        if currentGameState.hasFood(newPos[0], newPos[1]):
            score += 10
        if danger <= 1:
            score -= 20
        return score

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()
    # return betterEvaluationFunction(currentGameState)

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

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        return self.minimax_decision(gameState)
        util.raiseNotDefined()

    def minimax_decision(self, gameState):
        legalMoves = gameState.getLegalActions()
        scores = [self.value(gameState.generateSuccessor(0, action), 1, 0) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best
        return legalMoves[chosenIndex]

    def value(self, gameState, index, depth):
        if index > (gameState.getNumAgents() - 1):
            index = 0
            depth += 1
        legalMoves = gameState.getLegalActions(index)
        if gameState.isWin() or gameState.isLose() or depth == self.depth:
            return self.evaluationFunction(gameState)
        elif index == 0:
            scores = [self.value(gameState.generateSuccessor(index, action), index + 1, depth) for action in legalMoves]
            return max(scores)
        else:
            scores = [self.value(gameState.generateSuccessor(index, action), index + 1, depth) for action in legalMoves]
            return min(scores)

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        return self.minimax_decision(gameState)
        util.raiseNotDefined()

    def minimax_decision(self, gameState):
        legalMoves = gameState.getLegalActions()
        alpha = -1e10
        beta = 1e10
        bestScore = -1e10
        for action in legalMoves:
            bestScore = max(bestScore, self.value(gameState.generateSuccessor(0, action), 1, 0, alpha, beta))
            if self.value(gameState.generateSuccessor(0, action), 1, 0, alpha, beta) >= bestScore:
                bestAction = action
            if bestScore > beta:
                return action
            alpha = max(alpha, bestScore)
        return bestAction


    def value(self, gameState, index, depth, alpha, beta):
        if index > (gameState.getNumAgents() - 1):
            index = 0
            depth += 1
        legalMoves = gameState.getLegalActions(index)
        if gameState.isWin() or gameState.isLose() or depth == self.depth:
            return self.evaluationFunction(gameState)
        elif index == 0:
            return self.maxValue(gameState, index, legalMoves, depth, alpha, beta)
        else:
            return self.minValue(gameState, index, legalMoves, depth, alpha, beta)

    def maxValue(self, gameState, index, legalMoves, depth, alpha, beta):
        v = -1e10
        for action in legalMoves:
            v = max(v, self.value(gameState.generateSuccessor(index, action), index + 1, depth, alpha, beta))
            if v > beta:
                return v
            alpha = max(alpha, v)
        return v

    def minValue(self, gameState, index, legalMoves, depth, alpha, beta):
        v = 1e10
        for action in legalMoves:
            v = min(v, self.value(gameState.generateSuccessor(index, action), index + 1, depth, alpha, beta))
            if v < alpha:
                return v
            beta = min(beta, v)
        return v

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
        return self.minimax_decision(gameState)
        util.raiseNotDefined()

    def minimax_decision(self, gameState):
        legalMoves = gameState.getLegalActions()
        scores = [self.value(gameState.generateSuccessor(0, action), 1, 0) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best
        return legalMoves[chosenIndex]

    def value(self, gameState, index, depth):
        if index > (gameState.getNumAgents() - 1):
            index = 0
            depth += 1
        legalMoves = gameState.getLegalActions(index)
        if gameState.isWin() or gameState.isLose() or depth == self.depth:
            return self.evaluationFunction(gameState)
        elif index == 0:
            scores = [self.value(gameState.generateSuccessor(index, action), index + 1, depth) for action in legalMoves]
            return max(scores)
        else:
            scores = [self.value(gameState.generateSuccessor(index, action), index + 1, depth) for action in legalMoves]
            expectation = sum(scores)/len(scores)
            return expectation

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    I calculated the manhattan distance of the position to the nearest food 
    and the distance to the nearest ghost. I added the distance of the agent 
    to the ghost with the ghost fear time to represent the danger coefficient.
    The evaluation result is current score + 0.1 * danger coefficient - 2 * 
    distance to nearest food.
    """
    "*** YOUR CODE HERE ***"
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    dist = 0
    score = 0
    if len(newFood.asList()) != 0:
        foodDist = [manhattanDistance(newPos, food) for food in newFood.asList()]
        dist = min(foodDist)
    ghostInfo = [(ghost.getPosition(), ghost.scaredTimer) for ghost in newGhostStates]
    danger = manhattanDistance(newPos, ghostInfo[0][0]) + ghostInfo[0][1]
    for ghost in ghostInfo:
        if manhattanDistance(newPos, ghost[0]) + ghost[1] < danger:
            danger = manhattanDistance(newPos, ghost[0]) + ghost[1]
    score = currentGameState.getScore() + 0.1 * danger - 0.2 * dist
    if currentGameState.hasFood(newPos[0], newPos[1]):
        score += 10
    if danger <= 1:
        score -= 20
    return score
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
