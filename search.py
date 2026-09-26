"""
In search.py, you will implement generic search algorithms which are called 
by Pacman agents (in searchAgents.py).
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
     Returns the start state for the search problem 
     """
     util.raiseNotDefined()
    
  def isGoalState(self, state):
     """
       state: Search state
    
     Returns True if and only if the state is a valid goal state
     """
     util.raiseNotDefined()

  def getSuccessors(self, state):
     """
       state: Search state
     
     For a given state, this should return a list of triples, 
     (successor, action, stepCost), where 'successor' is a 
     successor to the current state, 'action' is the action
     required to get there, and 'stepCost' is the incremental 
     cost of expanding to that successor
     """
     util.raiseNotDefined()

  def getCostOfActions(self, actions):
     """
      actions: A list of actions to take
 
     This method returns the total cost of a particular sequence of actions.  The sequence must
     be composed of legal moves
     """
     util.raiseNotDefined()
           

def tinyMazeSearch(problem):
  """
  Returns a sequence of moves that solves tinyMaze.  For any other
  maze, the sequence of moves will be incorrect, so only use this for tinyMaze
  """
  from game import Directions
  s = Directions.SOUTH
  w = Directions.WEST
  return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):
  """
  DFS: explora primero el camino mas profundo (usa una PILA).
  """
  frontera = util.Stack()
  frontera.push((problem.getStartState(), []))
  visitados = set()

  while not frontera.isEmpty():
    estado, acciones = frontera.pop()
    if estado in visitados:
      continue
    if problem.isGoalState(estado):
      return acciones
    visitados.add(estado)
    for sucesor, accion, costo in problem.getSuccessors(estado):
      if sucesor not in visitados:
        frontera.push((sucesor, acciones + [accion]))
  return []

def breadthFirstSearch(problem):
  "BFS: explora primero los nodos mas cercanos al inicio (usa una COLA)."
  frontera = util.Queue()
  inicio = problem.getStartState()
  frontera.push((inicio, []))
  visitados = set([inicio])

  while not frontera.isEmpty():
    estado, acciones = frontera.pop()
    if problem.isGoalState(estado):
      return acciones
    for sucesor, accion, costo in problem.getSuccessors(estado):
      if sucesor not in visitados:
        visitados.add(sucesor)
        frontera.push((sucesor, acciones + [accion]))
  return []

def uniformCostSearch(problem):
  """
  UCS: saca siempre el nodo con MENOR costo acumulado.
      prioridad  f(n) = g(n)
  """
  frontera = util.PriorityQueue()
  contador = 0          # solo sirve para desempatar (el que entro primero sale primero)

  inicio = problem.getStartState()
  frontera.push((inicio, [], 0), (0, contador))
  mejor_g = {inicio: 0}           # el costo mas barato conocido para llegar a cada estado
  expandidos = set()              # estados que ya revisamos por completo

  while not frontera.isEmpty():
    estado, acciones, g = frontera.pop()

    if estado in expandidos:      # ya lo expandimos por un camino mas barato
      continue
    if problem.isGoalState(estado):
      return acciones
    expandidos.add(estado)

    for sucesor, accion, costo in problem.getSuccessors(estado):
      nuevo_g = g + costo
      if sucesor not in expandidos and nuevo_g < mejor_g.get(sucesor, float('inf')):
        mejor_g[sucesor] = nuevo_g
        contador += 1
        frontera.push((sucesor, acciones + [accion], nuevo_g), (nuevo_g, contador))
  return []

def nullHeuristic(state, problem=None):
  """
  A heuristic function estimates the cost from the current state to the nearest
  goal in the provided SearchProblem.  This heuristic is trivial.
  """
  return 0

def aStarSearch(problem, heuristic=nullHeuristic):
  """
  A*: saca siempre el nodo con MENOR  f(n) = g(n) + h(n)
      g(n) = lo que ya caminamos (costo real acumulado)
      h(n) = lo que creemos que falta (estimacion de la heuristica)
  """
  frontera = util.PriorityQueue()                 # 1. cola de prioridad
  contador = 0                                    # desempate: el que entro primero sale primero

  inicio = problem.getStartState()                # 2. empezamos en el estado inicial
  frontera.push((inicio, [], 0), (heuristic(inicio, problem), contador))
  mejor_g = {inicio: 0}                           # mejor g(n) conocido para cada estado
  expandidos = set()                              # 7. para no expandir dos veces el mismo estado

  while not frontera.isEmpty():
    estado, acciones, g = frontera.pop()          # el de menor f(n)

    if estado in expandidos:
      continue
    if problem.isGoalState(estado):               # 3. prueba de objetivo
      return acciones                             # 8. lista de acciones
    expandidos.add(estado)

    for sucesor, accion, costo in problem.getSuccessors(estado):   # 4. sucesores
      nuevo_g = g + costo                                           # 5. acumulamos g(n)
      if sucesor not in expandidos and nuevo_g < mejor_g.get(sucesor, float('inf')):
        mejor_g[sucesor] = nuevo_g                                  # encontramos un camino mejor
        f = nuevo_g + heuristic(sucesor, problem)                   # 6. f(n) = g(n) + h(n)
        contador += 1
        frontera.push((sucesor, acciones + [accion], nuevo_g), (f, contador))
  return []
  
# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch