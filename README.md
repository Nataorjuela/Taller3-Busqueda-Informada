# Taller-3-Búsqueda-Informada
Búsqueda informada con pac-man y heurística

## Comandos por actividad

> Todos los comandos se ejecutan desde la carpeta del proyecto, donde está `pacman.py`.
> En `openClassic` se usa `-k 0` para quitar el fantasma.

### Actividad 1 – Exploración del entorno

Jugar manualmente con las flechas o con W, A, S, D:

```bash
python pacman.py
```

Explorar los laberintos usados en el taller:

```bash
python pacman.py -l tinyMaze
python pacman.py -l mediumMaze
python pacman.py -l openClassic -k 0
```

### Actividad 2 – Búsqueda de costo uniforme (UCS)

```bash
python pacman.py -l tinyMaze -p SearchAgent -a fn=ucs
python pacman.py -l mediumMaze -p SearchAgent -a fn=ucs
python pacman.py -l openClassic -k 0 -p SearchAgent -a fn=ucs
```

### Actividad 3 – Implementación de A*

Prueba de que A* funciona (con heurística nula y con Manhattan):

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

### Resultados esperados

| Laberinto   | Algoritmo      | Costo | Nodos expandidos |
|-------------|----------------|-------|------------------|
| tinyMaze    | UCS            | 10    | 21               |
| tinyMaze    | A* + h(n) = 0  | 10    | 21               |
| tinyMaze    | A* + Manhattan | 10    | 10               |
| mediumMaze  | UCS            | 30    | 32               |
| openClassic | UCS            | 9     | 63               |
| openClassic | A* + h(n) = 0  | 9     | 63               |

### Notas

- Los resultados salen en las líneas `Path found with total cost of ...` y `Search nodes expanded: ...`.
- El tiempo aparece como `0.0 seconds` porque el juego redondea a una décima de segundo y estas búsquedas tardan menos de 1 milisegundo.
- En los laberintos que tienen comida sobrante (`tinyMaze`, `mediumMaze`, `openClassic`) aparece al final el error `Illegal action Stop`. Pac-Man llega a la meta, pero el juego no termina porque todavía queda comida y no le permite quedarse quieto. **No afecta los resultados.**

- ### Actividad 5 – Distancia Manhattan

```bash
python pacman.py -l tinyMaze -p SearchAgent -a fn=astar,heuristic=manhattanHeuristic
python pacman.py -l tinyMaze -p SearchAgent -a fn=astar,heuristic=nullHeuristic
```

### Resultados esperados

| Algoritmo      | Costo | Nodos expandidos |    Tiempo    |
|----------------|-------|------------------|--------------|
| UCS            | 10    | 21               |     0.0 s    |
| A* + Manhattan | 10    | 10               |     0.0 s    |


- ### Actividad 6 – Distancia Euclidiana
Para tener una mejor comparación se corrió en el mapa Openclassic

```bash
python pacman.py -l openclassic -p SearchAgent -a fn=astar,heuristic=manhattanHeuristic
python pacman.py -l openclassic -p SearchAgent -a fn=astar,heuristic=nullHeuristic
python pacman.py -l openclassic -p SearchAgent -a fn=astar,heuristic=euclideanHeuristic
```
| Algoritmo      | Costo | Nodos expandidos |    Tiempo    |
|----------------|-------|------------------|--------------|
| h(n)=0         | 9     | 63               |     0.0 s    |
| Manhattan      | 9     | 27               |     0.0 s    |
| Euclidiana     | 9     | 31               |     0.0 s    |

RESPUESTA: La distancia Manhattan representa mejor el movimiento de Pac-Man porque calcula la distancia exacta sobre la cuadrícula considerando únicamente desplazamientos ortogonales (Norte, Sur, Este y Oeste), lo que corresponde a la solución exacta de un problema relajado sin paredes. A diferencia de la distancia Euclidiana —la cual subestima en mayor medida el costo real al asumir trayectos diagonales en línea recta que Pac-Man no puede ejecutar. 





