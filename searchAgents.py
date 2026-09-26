"""
This file contains all of the agents that can be selected to 
control Pacman.  To select an agent, use the '-p' option
when running pacman.py.  Arguments can be passed to your agent
using '-a'.  For example, to load a SearchAgent that uses
depth first search (dfs), run the following command:

> python pacman.py -p SearchAgent -a searchFunction=depthFirstSearch

Commands to invoke other search strategies can be found in the 
project description.

Please only change the parts of the file you are asked to.
Look for the lines that say

"*** YOUR CODE HERE ***"

The parts you fill in start about 3/4 of the way down.  Follow the
project description for details.

Good luck and happy searching!
"""

from game import Directions
from game import Agent
from game import Actions
import util
import time
import search
import searchAgents

class GoWestAgent(Agent):
  "An agent that goes West until it can't."
  
  def getAction(self, state):
    "The agent receives a GameState (defined in pacman.py)."
    if Directions.WEST in state.getLegalPacmanActions():
      return Directions.WEST
    else:
      return Directions.STOP

#######################################################
# This portion is written for you, but will only work #
#       after you fill in parts of search.py          #
#######################################################

class SearchAgent(Agent):
  """
  This very general search agent finds a path using a supplied search algorithm for a
  supplied search problem, then returns actions to follow that path.
  
  As a default, this agent runs DFS on a PositionSearchProblem to find location (1,1)
  
  Options for fn include:
    depthFirstSearch or dfs
    breadthFirstSearch or bfs
    
  
  Note: You should NOT change any code in SearchAgent
  """
    
  def __init__(self, fn='depthFirstSearch', prob='PositionSearchProblem', heuristic='nullHeuristic'):
    # Warning: some advanced Python magic is employed below to find the right functions and problems
    
    # Get the search function from the name and heuristic
    if fn not in dir(search): 
      raise AttributeError(fn + ' is not a search function in search.py.')
    func = getattr(search, fn)
    if 'heuristic' not in func.__code__.co_varnames:
      print(('[SearchAgent] using function ' + fn)) 
      self.searchFunction = func
    else:
      if heuristic in dir(searchAgents):
        heur = getattr(searchAgents, heuristic)
      elif heuristic in dir(search):
        heur = getattr(search, heuristic)
      else:
        raise AttributeError(heuristic + ' is not a function in searchAgents.py or search.py.')
      print(('[SearchAgent] using function %s and heuristic %s' % (fn, heuristic))) 
      # Note: this bit of Python trickery combines the search algorithm and the heuristic
      self.searchFunction = lambda x: func(x, heuristic=heur)
      
    # Get the search problem type from the name
    if prob not in dir(searchAgents) or not prob.endswith('Problem'): 
      raise AttributeError(prob + ' is not a search problem type in SearchAgents.py.')
    self.searchType = getattr(searchAgents, prob)
    print(('[SearchAgent] using problem type ' + prob)) 
    
  def registerInitialState(self, state):
    """
    This is the first time that the agent sees the layout of the game board. Here, we
    choose a path to the goal.  In this phase, the agent should compute the path to the
    goal and store it in a local variable.  All of the work is done in this method!
    
    state: a GameState object (pacman.py)
    """
    if self.searchFunction is None: raise Exception("No search function provided for SearchAgent")
    starttime = time.time()
    problem = self.searchType(state) # Makes a new search problem
    self.actions  = self.searchFunction(problem) # Find a path
    totalCost = problem.getCostOfActions(self.actions)
    print(('Path found with total cost of %d in %.1f seconds' % (totalCost, time.time() - starttime)))
    if '_expanded' in dir(problem): print(('Search nodes expanded: %d' % problem._expanded))
    
  def getAction(self, state):
    """
    Returns the next action in the path chosen earlier (in registerInitialState).  Return
    Directions.STOP if there is no further action to take.
    
    state: a GameState object (pacman.py)
    """
    if 'actionIndex' not in dir(self): self.actionIndex = 0
    i = self.actionIndex
    self.actionIndex += 1
    if i < len(self.actions):
      return self.actions[i]    
    else:
      return Directions.STOP

class PositionSearchProblem(search.SearchProblem):
  """
  A search problem defines the state space, start state, goal test,
  successor function and cost function.  This search problem can be 
  used to find paths to a particular point on the pacman board.
  
  The state space consists of (x,y) positions in a pacman game.
  
  Note: this search problem is fully specified; you should NOT change it.
  """
  
  def __init__(self, gameState, costFn = lambda x: 1, goal=(1,1), start=None, warn=True):
    """
    Stores the start and goal.  
    
    gameState: A GameState object (pacman.py)
    costFn: A function from a search state (tuple) to a non-negative number
    goal: A position in the gameState
    """
    self.walls = gameState.getWalls()
    self.startState = gameState.getPacmanPosition()
    if start != None: self.startState = start
    self.goal = goal
    self.costFn = costFn
    if warn and (gameState.getNumFood() != 1 or not gameState.hasFood(*goal)):
      print('Warning: this does not look like a regular search maze')

    # For display purposes
    self._visited, self._visitedlist, self._expanded = {}, [], 0

  def getStartState(self):
    return self.startState

  def isGoalState(self, state):
     isGoal = state == self.goal 
     
     # For display purposes only
     if isGoal:
       self._visitedlist.append(state)
       import __main__
       if '_display' in dir(__main__):
         if 'drawExpandedCells' in dir(__main__._display): #@UndefinedVariable
           __main__._display.drawExpandedCells(self._visitedlist) #@UndefinedVariable
       
     return isGoal   
   
  def getSuccessors(self, state):
    """
    Returns successor states, the actions they require, and a cost of 1.
    
     As noted in search.py:
         For a given state, this should return a list of triples, 
     (successor, action, stepCost), where 'successor' is a 
     successor to the current state, 'action' is the action
     required to get there, and 'stepCost' is the incremental 
     cost of expanding to that successor
    """
    
    successors = []
    for action in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
      x,y = state
      dx, dy = Actions.directionToVector(action)
      nextx, nexty = int(x + dx), int(y + dy)
      if not self.walls[nextx][nexty]:
        nextState = (nextx, nexty)
        cost = self.costFn(nextState)
        successors.append( ( nextState, action, cost) )
        
    # Bookkeeping for display purposes
    self._expanded += 1 
    if state not in self._visited:
      self._visited[state] = True
      self._visitedlist.append(state)
      
    return successors

  def getCostOfActions(self, actions):
    """
    Returns the cost of a particular sequence of actions.  If those actions
    include an illegal move, return 999999
    """
    if actions is None: return 999999
    x,y= self.getStartState()
    cost = 0
    for action in actions:
      # Check figure out the next state and see whether its' legal
      dx, dy = Actions.directionToVector(action)
      x, y = int(x + dx), int(y + dy)
      if self.walls[x][y]: return 999999
      cost += self.costFn((x,y))
    return cost

class StayEastSearchAgent(SearchAgent):
  """
  An agent for position search with a cost function that penalizes being in
  positions on the West side of the board.  
  
  The cost function for stepping into a position (x,y) is 1/2^x.
  """
  def __init__(self):
      self.searchFunction = search.uniformCostSearch
      costFn = lambda pos: .5 ** pos[0] 
      self.searchType = lambda state: PositionSearchProblem(state, costFn)
      
class StayWestSearchAgent(SearchAgent):
  """
  An agent for position search with a cost function that penalizes being in
  positions on the East side of the board.  
  
  The cost function for stepping into a position (x,y) is 2^x.
  """
  def __init__(self):
      self.searchFunction = search.uniformCostSearch
      costFn = lambda pos: 2 ** pos[0] 
      self.searchType = lambda state: PositionSearchProblem(state, costFn)

def manhattanHeuristic(position, problem, info={}):
  "The Manhattan distance heuristic for a PositionSearchProblem"
  xy1 = position
  xy2 = problem.goal
  return abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])

def euclideanHeuristic(position, problem, info={}):
  "The Euclidean distance heuristic for a PositionSearchProblem"
  xy1 = position
  xy2 = problem.goal
  return ( (xy1[0] - xy2[0]) ** 2 + (xy1[1] - xy2[1]) ** 2 ) ** 0.5

#####################################################
# This portion is incomplete.  Time to write code!  #
#####################################################

class CornersProblem(search.SearchProblem):
  """
  This search problem finds paths through all four corners of a layout.

  You must select a suitable state space and successor function
  """
  
  def __init__(self, startingGameState):
    """
    Stores the walls, pacman's starting position and corners.
    """
    self.walls = startingGameState.getWalls()
    self.startingPosition = startingGameState.getPacmanPosition()
    top, right = self.walls.height-2, self.walls.width-2 
    self.corners = ((1,1), (1,top), (right, 1), (right, top))
    for corner in self.corners:
      if not startingGameState.hasFood(*corner):
        print('Warning: no food in corner ' + str(corner))
    self._expanded = 0 # Number of search nodes expanded
    
    
  def getStartState(self):
    """
    Estado = (posicion, esquinas_visitadas)
      posicion           -> (x, y) de Pac-Man
      esquinas_visitadas -> tupla de 4 True/False, en el mismo orden de self.corners
    Ej: ((5,4), (True, False, False, False)) = estoy en (5,4) y solo visite la 1a esquina.
    """
    visitadas = tuple(esquina == self.startingPosition for esquina in self.corners)
    return (self.startingPosition, visitadas)

  def isGoalState(self, state):
    "Ganamos cuando las 4 esquinas estan visitadas."
    posicion, visitadas = state
    return all(visitadas)

  def getSuccessors(self, state):
    """
    Para cada direccion posible: si no hay pared, Pac-Man se mueve
    y, si cae en una esquina, la marcamos como visitada. Costo = 1.
    """
    successors = []
    (x, y), visitadas = state
    for action in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
      dx, dy = Actions.directionToVector(action)
      nextx, nexty = int(x + dx), int(y + dy)
      if not self.walls[nextx][nexty]:
        nuevaPos = (nextx, nexty)
        nuevasVisitadas = tuple(v or (esquina == nuevaPos)
                                for v, esquina in zip(visitadas, self.corners))
        successors.append(((nuevaPos, nuevasVisitadas), action, 1))

    self._expanded += 1
    return successors

  def getCostOfActions(self, actions):
    """
    Returns the cost of a particular sequence of actions.  If those actions
    include an illegal move, return 999999.  This is implemented for you.
    """
    if actions is None: return 999999
    x,y= self.startingPosition
    for action in actions:
      dx, dy = Actions.directionToVector(action)
      x, y = int(x + dx), int(y + dy)
      if self.walls[x][y]: return 999999
    return len(actions)


def esquinasPendientes(state, problem):
  "Lista de las esquinas que todavia NO se han visitado."
  posicion, visitadas = state
  return [c for c, v in zip(problem.corners, visitadas) if not v]

def cornersHeuristicBasica(state, problem):
  """
  Heuristica basica (la que sugiere la guia):
     h(n) = max  d_M(n, c)   para c en las esquinas pendientes
  "Por lo menos tengo que llegar a la esquina mas lejana."
  """
  posicion = state[0]
  pendientes = esquinasPendientes(state, problem)
  if not pendientes:
    return 0
  return max(util.manhattanDistance(posicion, c) for c in pendientes)

def cornersHeuristic(state, problem):
  """
  Heuristica propuesta: "ruta Manhattan mas corta por TODAS las esquinas pendientes".

  Imaginamos que el laberinto NO tiene paredes. En ese mundo sin paredes,
  probamos todos los ordenes posibles de visitar las esquinas que faltan
  (como mucho 4! = 24 ordenes) y nos quedamos con el recorrido mas corto.

     h(n) = min  [ d_M(n, c1) + d_M(c1, c2) + ... + d_M(c_{k-1}, c_k) ]
          sobre todos los ordenes (c1, ..., ck) de las esquinas pendientes

  Como con paredes el camino real solo puede ser igual o mas largo,
  esta h nunca sobreestima (es admisible) y ademas es consistente.
  """
  from itertools import permutations
  posicion = state[0]
  pendientes = esquinasPendientes(state, problem)
  if not pendientes:
    return 0

  mejor = float('inf')
  for orden in permutations(pendientes):
    total = 0
    actual = posicion
    for esquina in orden:
      total += util.manhattanDistance(actual, esquina)
      actual = esquina
    mejor = min(mejor, total)
  heuristicValue = mejor
  return heuristicValue

class AStarCornersAgent(SearchAgent):
  "A SearchAgent for FoodSearchProblem using A* and your foodHeuristic"
  def __init__(self):
    self.searchFunction = lambda prob: search.aStarSearch(prob, cornersHeuristic)
    self.searchType = CornersProblem

class FoodSearchProblem:
  """
  A search problem associated with finding the a path that collects all of the 
  food (dots) in a Pacman game.
  
  A search state in this problem is a tuple ( pacmanPosition, foodGrid ) where
    pacmanPosition: a tuple (x,y) of integers specifying Pacman's position
    foodGrid:       a Grid (see game.py) of either True or False, specifying remaining food 
  """
  def __init__(self, startingGameState):
    self.start = (startingGameState.getPacmanPosition(), startingGameState.getFood())
    self.walls = startingGameState.getWalls()
    self.startingGameState = startingGameState
    self._expanded = 0
    self.heuristicInfo = {} # A dictionary for the heuristic to store information
      
  def getStartState(self):
    return self.start
  
  def isGoalState(self, state):
    return state[1].count() == 0

  def getSuccessors(self, state):
    "Returns successor states, the actions they require, and a cost of 1."
    successors = []
    self._expanded += 1
    for direction in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
      x,y = state[0]
      dx, dy = Actions.directionToVector(direction)
      nextx, nexty = int(x + dx), int(y + dy)
      if not self.walls[nextx][nexty]:
        nextFood = state[1].copy()
        nextFood[nextx][nexty] = False
        successors.append( ( ((nextx, nexty), nextFood), direction, 1) )
    return successors

  def getCostOfActions(self, actions):
    """Returns the cost of a particular sequence of actions.  If those actions
    include an illegal move, return 999999"""
    x,y= self.getStartState()[0]
    cost = 0
    for action in actions:
      # figure out the next state and see whether it's legal
      dx, dy = Actions.directionToVector(action)
      x, y = int(x + dx), int(y + dy)
      if self.walls[x][y]:
        return 999999
      cost += 1
    return cost

class AStarFoodSearchAgent(SearchAgent):
  "A SearchAgent for FoodSearchProblem using A* and your foodHeuristic"
  def __init__(self):
    self.searchFunction = lambda prob: search.aStarSearch(prob, foodHeuristic)
    self.searchType = FoodSearchProblem

def foodHeuristicBasica(state, problem):
  """
  Heuristica 1 (la que sugiere la guia):
     h(n) = max  d_M(n, f)   para f en la comida restante
  "Por lo menos tengo que caminar hasta la comida mas lejana (en linea Manhattan)."
  """
  position, foodGrid = state
  comidas = foodGrid.asList()
  if not comidas:
    return 0
  return max(util.manhattanDistance(position, f) for f in comidas)

def distanciasDesde(origen, walls):
  """
  BFS sobre el laberinto: devuelve un diccionario {celda: distancia REAL
  (respetando paredes) desde 'origen' hasta esa celda}.
  """
  distancias = {origen: 0}
  cola = util.Queue()
  cola.push(origen)
  while not cola.isEmpty():
    x, y = cola.pop()
    for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
      vecino = (x + dx, y + dy)
      if not walls[vecino[0]][vecino[1]] and vecino not in distancias:
        distancias[vecino] = distancias[(x, y)] + 1
        cola.push(vecino)
  return distancias

def distanciaLaberinto(a, b, problem, usarCache=True):
  """
  Distancia REAL entre a y b dentro del laberinto (respetando paredes).
  Con usarCache=True guarda el BFS de cada punto en problem.heuristicInfo
  para no repetir el mismo calculo miles de veces.
  """
  if not usarCache:
    return distanciasDesde(a, problem.walls)[b]
  if a not in problem.heuristicInfo:                     # si no lo hemos calculado...
    problem.heuristicInfo[a] = distanciasDesde(a, problem.walls)
  return problem.heuristicInfo[a][b]                     # ...si ya existe, lo reutilizamos

def foodHeuristic(state, problem, usarCache=True):
  """
  Heuristica 2 (propuesta): "las dos comidas mas separadas".

  Idea: de toda la comida que queda, busco las dos comidas A y B que estan
  mas lejos una de la otra (en distancia real del laberinto, d_L).
  Pac-Man tiene que pasar por las dos, asi que como minimo debe:
     1) llegar a la mas cercana de las dos, y
     2) caminar de esa hasta la otra.

     h(n) = max   [ min( d_L(p, A), d_L(p, B) ) + d_L(A, B) ]
          A,B en F
  (Si A = B, el termino queda d_L(p, A): la comida mas lejana, igual que la heuristica 1
   pero respetando paredes. Por eso esta h siempre es >= que la heuristica 1.)
  """
  position, foodGrid = state
  comidas = foodGrid.asList()
  if not comidas:
    return 0

  mejor = 0
  for i in range(len(comidas)):
    for j in range(i, len(comidas)):
      A, B = comidas[i], comidas[j]
      llegar = min(distanciaLaberinto(position, A, problem, usarCache),
                   distanciaLaberinto(position, B, problem, usarCache))
      cruzar = distanciaLaberinto(A, B, problem, usarCache)
      mejor = max(mejor, llegar + cruzar)
  return mejor

def foodHeuristicSinCache(state, problem):
  "Igual que foodHeuristic, pero recalculando los BFS cada vez (solo para comparar tiempos)."
  return foodHeuristic(state, problem, usarCache=False)

class ClosestDotSearchAgent(SearchAgent):
  "Search for all food using a sequence of searches"
  def registerInitialState(self, state):
    self.actions = []
    currentState = state
    while(currentState.getFood().count() > 0): 
      nextPathSegment = self.findPathToClosestDot(currentState) # The missing piece
      self.actions += nextPathSegment
      for action in nextPathSegment: 
        legal = currentState.getLegalActions()
        if action not in legal: 
          t = (str(action), str(currentState))
          raise Exception('findPathToClosestDot returned an illegal move: %s!\n%s' % t)
        currentState = currentState.generateSuccessor(0, action)
    self.actionIndex = 0
    print('Path found with cost %d.' % len(self.actions))
    
  def findPathToClosestDot(self, gameState):
    "Returns a path (a list of actions) to the closest dot, starting from gameState"
    # Here are some useful elements of the startState
    startPosition = gameState.getPacmanPosition()
    food = gameState.getFood()
    walls = gameState.getWalls()
    problem = AnyFoodSearchProblem(gameState)

  
class AnyFoodSearchProblem(PositionSearchProblem):
  """
    A search problem for finding a path to any food.
    
    This search problem is just like the PositionSearchProblem, but
    has a different goal test, which you need to fill in below.  The
    state space and successor function do not need to be changed.
    
    The class definition above, AnyFoodSearchProblem(PositionSearchProblem),
    inherits the methods of the PositionSearchProblem.
    
    You can use this search problem to help you fill in 
    the findPathToClosestDot method.
  """

  def __init__(self, gameState):
    "Stores information from the gameState.  You don't need to change this."
    # Store the food for later reference
    self.food = gameState.getFood()

    # Store info for the PositionSearchProblem (no need to change this)
    self.walls = gameState.getWalls()
    self.startState = gameState.getPacmanPosition()
    self.costFn = lambda x: 1
    self._visited, self._visitedlist, self._expanded = {}, [], 0
    
  def isGoalState(self, state):
    """
    The state is Pacman's position. Fill this in with a goal test
    that will complete the problem definition.
    """
    x,y = state
    

##################
# Mini-contest 1 #
##################

class ApproximateSearchAgent(Agent):
  "Implement your contest entry here.  Change anything but the class name."
  
  def registerInitialState(self, state):
    "This method is called before any moves are made."
    
  def getAction(self, state):
    """
    From game.py: 
    The Agent will receive a GameState and must return an action from 
    Directions.{North, South, East, West, Stop}
    """ 
    
def mazeDistance(point1, point2, gameState):
  """
  Returns the maze distance between any two points, using the search functions
  you have already built.  The gameState can be any game state -- Pacman's position
  in that state is ignored.
  
  Example usage: mazeDistance( (2,4), (5,6), gameState)
  
  This might be a useful helper function for your ApproximateSearchAgent.
  """
  x1, y1 = point1
  x2, y2 = point2
  walls = gameState.getWalls()
  assert not walls[x1][y1], 'point1 is a wall: ' + point1
  assert not walls[x2][y2], 'point2 is a wall: ' + str(point2)
  prob = PositionSearchProblem(gameState, start=point1, goal=point2, warn=False)
  return len(search.bfs(prob))