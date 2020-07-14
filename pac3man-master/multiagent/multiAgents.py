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

from util import manhattanDistance as manhattan


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
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best

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
        currFood = currentGameState.getFood()
        Fooddist = []
        for food in currFood.asList():
            if Directions.STOP in action:  # if action is stop then do not pursue it return high -ve value
                return -99999999
            if manhattan(newPos, food) == 0:  # if next position is food then pursue it. Reciprocal will give high value
                Fooddist.append(1)
            else:
                Fooddist.append(manhattan(newPos, food))  # store distances to food in array

        for ghost in newGhostStates:
            if manhattan(newPos, ghost.getPosition()) == 0:  # Avoid if ghost is in the next position is ghost
                return -9999999

        return currentGameState.getScore() + (1 / min(Fooddist))  # maximize score and reduce distance to next food


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

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def minimax(self, state, agent, depth, player):
        minimize_move = 0
        maximize_move = 0

        if state.isLose() or state.isWin() or depth == self.depth:  # Base Cases
            return self.evaluationFunction(state), 0  # returns the value of that evaluation

        if player:  # Pacman's move to maximize
            val = -9999999
            for each in state.getLegalActions(agent):
                successor = state.generateSuccessor(agent, each)
                points = self.minimax(successor, agent + 1, depth, False)[0]  # Iterates to min move
                if points > val:
                    val, maximize_move = points, each
            return val, maximize_move  # Maximize agent moves

        else:  # Other Agents, Player will be False
            val = 9999999
            for each in state.getLegalActions(agent):
                if agent < state.getNumAgents() - 1:  # Keeps recursing through same depth level
                    successor = state.generateSuccessor(agent, each)
                    points = self.minimax(successor, agent + 1, depth, False)[0]
                else:  # Increases the depth and recurses (Pacman's turn)
                    successor = state.generateSuccessor(agent, each)
                    points = self.minimax(successor, 0, depth + 1, True)[0]
                if points < val:
                    val, minimize_move = points, each
            return val, minimize_move  # Minimizing agent moves

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
        return (self.minimax(gameState, 0, 0, True)[1])  # Calls minimax on pacman with player = True


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)

      alpha: MAX's best option on path to root
      beta: MIN's best option on path to root
      """

    def max_value(self, state, agent, depth, alpha, beta):
        v = -999999
        move = 0

        if depth == self.depth or state.isLose() or state.isWin() or not state.getLegalActions(0): # Base Case for Pacman
            return self.evaluationFunction(state), 0

        for each in state.getLegalActions(0):
            successor = state.generateSuccessor(0, each)
            nv = self.min_value(successor, agent + 1, depth, alpha, beta)[0]
            if nv > v:                              # Finds max value from recursion above
                v = nv
                move = each
            if v > beta:                               # if value is greater than beta then prune
                return v, move
            alpha = max(alpha, v)                   # Save alpha
        return v, move

    def min_value(self, state, agent, depth, alpha, beta):
        v = 999999
        move = 0

        if depth == self.depth or state.isLose() or state.isWin() or not state.getLegalActions(agent): # Base case for ghots
            return self.evaluationFunction(state), 0

        for each in state.getLegalActions(agent):
            if agent == state.getNumAgents() - 1:               # If final ghost then find max player
                successor = state.generateSuccessor(agent, each)
                nv = self.max_value(successor, 0, depth + 1, alpha, beta)[0]
            else:
                successor = state.generateSuccessor(agent, each)            # Same level if other ghosts
                nv = self.min_value(successor, agent + 1, depth, alpha, beta)[0]

            if nv < v:                              # If score is min then save the move
                v = nv
                move = each
            if v < alpha:                              # If value is less than alpha then prune
                return v, move
            beta = min(beta, v)                     # Save beta

        return v, move

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()
        return self.max_value(gameState, 0, 0, -9999, 9999)[1]


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def maxVal(self, state, agent, depth):
        val = -9999999
        move = 0
        if depth == self.depth or state.isWin():            # Base case
            return self.evaluationFunction(state), 0
        for each in state.getLegalActions(agent):
            successor = state.generateSuccessor(0, each)
            v = self.expVal(successor, agent + 1, depth)[0]
            if val < v:                                     # Finds max value from recursion above
                val = v
                move = each
        return val, move

    def expVal(self, state, agent, depth):
        total = 0
        score = []
        if depth == self.depth or state.isLose():
            return self.evaluationFunction(state), 0
        for each in state.getLegalActions(agent):
            successor = state.generateSuccessor(agent, each)
            if agent == state.getNumAgents() - 1:               # if last ghost then find max value again
                score.append(self.maxVal(successor, 0, depth + 1)[0])
            else:
                score.append(self.expVal(successor, agent + 1, depth)[0])
        for one in score:
            total = total + (one / len(score))          # save all the probabilities
        return total, 0

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()
        return self.maxVal(gameState, 0, 0)[1]


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    # util.raiseNotDefined()
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    "*** YOUR CODE HERE ***"
    currFood = currentGameState.getFood()
    Fooddist = []
    for food in currFood.asList():
        if manhattan(newPos, food) == 0:  # if next position is food then pursue it. Reciprocal will give high value
            Fooddist.append(1)
        else:
            Fooddist.append(manhattan(newPos, food))  # store distances to food in array

    for ghost in newGhostStates:
        if manhattan(newPos, ghost.getPosition()) == 0:  # Avoid if ghost is in the next position is ghost
            return -9999999

    return currentGameState.getScore() + (1 / min(Fooddist)) + 1 / len(
        newScaredTimes)  # maximize score and reduce distance to next food


# Abbreviation
better = betterEvaluationFunction

