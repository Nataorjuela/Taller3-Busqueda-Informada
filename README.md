# Taller 3 – Búsqueda Informada

Búsqueda informada con Pac-Man: algoritmo A* y diseño de heurísticas.

## Integrantes del equipo

- Jimmy Millan
- Santiago León
- Natalia Orjuela

## Requisitos

- Python 3.
- La ventana gráfica usa `tkinter`: en Windows viene incluido con Python; en Linux puede requerir `sudo apt install python3-tk`.
- Si no se puede abrir la ventana, se puede agregar `-q` a cualquier comando para ver los resultados solo en la consola.

## Archivos modificados

| Archivo | Qué se implementó |
|---|---|
| `search.py` | `uniformCostSearch` (UCS), `aStarSearch` (A*), además de DFS y BFS |
| `searchAgents.py` | `CornersProblem`, `cornersHeuristicBasica`, `cornersHeuristic`, `foodHeuristicBasica`, `foodHeuristic`, `foodHeuristicSinCache` |
| `experimentos.py` | Script que corre todos los experimentos y genera `resultados.csv` |

## Comandos por actividad

> Todos los comandos se ejecutan desde la carpeta del proyecto, donde está `pacman.py`.
> En `openClassic` y `testClassic` se usa `-k 0` para quitar el fantasma.

### Actividad 1 – Exploración del entorno

Jugar manualmente con las flechas o con W, A, S, D:

```bash
python pacman.py
```

Explorar los laberintos usados en el taller:

```bash
python pacman.py -l tinyMaze
python pacman.py -l openClassic -k 0
python pacman.py -l tinyCorners
python pacman.py -l testClassic -k 0
```

### Actividad 2 – Búsqueda de costo uniforme (UCS)

```bash
python pacman.py -l tinyMaze -p SearchAgent -a fn=ucs
python pacman.py -l mediumMaze -p SearchAgent -a fn=ucs
python pacman.py -l openClassic -k 0 -p SearchAgent -a fn=ucs
```

### Actividad 3 – Implementación de A*

```bash
python pacman.py -l tinyMaze -p SearchAgent -a fn=astar,heuristic=nullHeuristic
python pacman.py -l tinyMaze -p SearchAgent -a fn=astar,heuristic=manhattanHeuristic
```

### Actividad 4 – A* con heurística nula vs UCS

```bash
python pacman.py -l tinyMaze -p SearchAgent -a fn=ucs
python pacman.py -l tinyMaze -p SearchAgent -a fn=astar,heuristic=nullHeuristic

python pacman.py -l openClassic -k 0 -p SearchAgent -a fn=ucs
python pacman.py -l openClassic -k 0 -p SearchAgent -a fn=astar,heuristic=nullHeuristic
```

### Actividad 5 – Distancia Manhattan

```bash
python pacman.py -l tinyMaze -p SearchAgent -a fn=astar,heuristic=manhattanHeuristic
python pacman.py -l openClassic -k 0 -p SearchAgent -a fn=astar,heuristic=manhattanHeuristic
```

Para ver mejor las casillas exploradas (en rojo), se puede agrandar la ventana con `-z 2`.

### Actividad 6 – Distancia Euclidiana y comparación de heurísticas

```bash
python pacman.py -l openClassic -k 0 -p SearchAgent -a fn=astar,heuristic=nullHeuristic
python pacman.py -l openClassic -k 0 -p SearchAgent -a fn=astar,heuristic=manhattanHeuristic
python pacman.py -l openClassic -k 0 -p SearchAgent -a fn=astar,heuristic=euclideanHeuristic
```

### Actividad 7 – Problema de las cuatro esquinas

```bash
python pacman.py -l tinyCorners -p SearchAgent -a fn=ucs,prob=CornersProblem
python pacman.py -l openClassic -k 0 -p SearchAgent -a fn=ucs,prob=CornersProblem
```

### Actividad 8 – Heurísticas para las esquinas

Heurística básica (esquina pendiente más lejana):

```bash
python pacman.py -l tinyCorners -p SearchAgent -a fn=astar,prob=CornersProblem,heuristic=cornersHeuristicBasica
```

Heurística propuesta (ruta Manhattan por todas las esquinas):

```bash
python pacman.py -l tinyCorners -p AStarCornersAgent
```

### Actividad 9 – Experimento comparativo

```bash
python pacman.py -l tinyCorners -p SearchAgent -a fn=ucs,prob=CornersProblem
python pacman.py -l tinyCorners -p SearchAgent -a fn=astar,prob=CornersProblem,heuristic=nullHeuristic
python pacman.py -l tinyCorners -p SearchAgent -a fn=astar,prob=CornersProblem,heuristic=cornersHeuristicBasica
python pacman.py -l tinyCorners -p AStarCornersAgent

python pacman.py -l openClassic -k 0 -p SearchAgent -a fn=ucs,prob=CornersProblem
python pacman.py -l openClassic -k 0 -p SearchAgent -a fn=astar,prob=CornersProblem,heuristic=nullHeuristic
python pacman.py -l openClassic -k 0 -p SearchAgent -a fn=astar,prob=CornersProblem,heuristic=cornersHeuristicBasica
python pacman.py -l openClassic -k 0 -p AStarCornersAgent
```

### Actividades 10 y 11 – Búsqueda de todos los alimentos

```bash
python pacman.py -l testClassic -k 0 -p SearchAgent -a fn=astar,prob=FoodSearchProblem,heuristic=nullHeuristic
python pacman.py -l testClassic -k 0 -p SearchAgent -a fn=astar,prob=FoodSearchProblem,heuristic=foodHeuristicBasica
python pacman.py -l testClassic -k 0 -p AStarFoodSearchAgent

python pacman.py -l tinyCorners -p SearchAgent -a fn=astar,prob=FoodSearchProblem,heuristic=nullHeuristic
python pacman.py -l tinyCorners -p SearchAgent -a fn=astar,prob=FoodSearchProblem,heuristic=foodHeuristicBasica
python pacman.py -l tinyCorners -p AStarFoodSearchAgent
```

Comparación con y sin caché (`problem.heuristicInfo`):

```bash
python pacman.py -l testClassic -k 0 -p SearchAgent -a fn=astar,prob=FoodSearchProblem,heuristic=foodHeuristicSinCache
python pacman.py -l testClassic -k 0 -p AStarFoodSearchAgent
```

### Todos los experimentos de una vez

Corre todos los casos sin abrir la ventana, mide el tiempo en milisegundos y genera `resultados.csv`:

```bash
python experimentos.py
```

## Resultados esperados

### Una sola meta: llegar a la casilla (1,1)

| Laberinto   | Algoritmo       | Costo | Nodos expandidos |
|-------------|-----------------|-------|------------------|
| tinyMaze    | UCS             | 10    | 21               |
| tinyMaze    | A* + h(n) = 0   | 10    | 21               |
| tinyMaze    | A* + Manhattan  | 10    | 10               |
| tinyMaze    | A* + Euclidiana | 10    | 10               |
| mediumMaze  | UCS             | 30    | 32               |
| openClassic | UCS             | 9     | 63               |
| openClassic | A* + h(n) = 0   | 9     | 63               |
| openClassic | A* + Manhattan  | 9     | 27               |
| openClassic | A* + Euclidiana | 9     | 31               |

### Problema de las esquinas

| Laberinto   | Método                    | Costo | Nodos expandidos | R = N_UCS / N_A* |
|-------------|---------------------------|-------|------------------|------------------|
| tinyCorners | UCS                       | 22    | 295              | 1.00             |
| tinyCorners | A* + h = 0                | 22    | 295              | 1.00             |
| tinyCorners | A* + heurística básica    | 22    | 147              | 2.01             |
| tinyCorners | A* + heurística propuesta | 22    | 77               | 3.83             |
| openClassic | UCS                       | 37    | 1037             | 1.00             |
| openClassic | A* + h = 0                | 37    | 1037             | 1.00             |
| openClassic | A* + heurística básica    | 37    | 367              | 2.83             |
| openClassic | A* + heurística propuesta | 37    | 37               | 28.03            |

### Búsqueda de toda la comida

| Laberinto   | Heurística                 | Costo | Nodos expandidos |
|-------------|----------------------------|-------|------------------|
| testClassic | h(n) = 0                   | 16    | 2598             |
| testClassic | Heurística 1 (Manhattan)   | 16    | 702              |
| testClassic | Heurística 2 (con caché)   | 16    | 209              |
| tinyCorners | h(n) = 0                   | 22    | 295              |
| tinyCorners | Heurística 1 (Manhattan)   | 22    | 147              |
| tinyCorners | Heurística 2 (con caché)   | 22    | 77               |

Con y sin caché se expanden los mismos nodos, pero con caché la heurística 2 es unas 19 veces más rápida en `testClassic`.

## Notas

- Los resultados salen en las líneas `Path found with total cost of ...` y `Search nodes expanded: ...`.
- `pacman.py` muestra el tiempo con un solo decimal en segundos, por eso casi siempre aparece `0.0 seconds`. Para medir en milisegundos se usa `experimentos.py`.
- En los laberintos con comida sobrante (`tinyMaze`, `mediumMaze`, `openClassic`) aparece al final el error `Illegal action Stop`. Pac-Man llega a la meta, pero el juego no termina porque todavía queda comida y no le permite quedarse quieto. **No afecta los resultados.** En `tinyCorners` y `testClassic` no pasa, porque Pac-Man se come toda la comida y el juego termina con "Win".
- El laberinto `mediumCorners` que viene en el proyecto deja a Pac-Man encerrado (ninguna esquina es alcanzable), por eso el problema de las esquinas se evaluó en `tinyCorners` y `openClassic`.
- El análisis completo (admisibilidad, consistencia, gráficas y conclusiones) está en `informe.pdf`.