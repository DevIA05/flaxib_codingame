import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.
def maze_list():
    maze = []
    w, h = [int(i) for i in input().split()]
    for ligne in range(h):
        row = input()
        ligne_list = []
        for index in range(0, len(row)):
            cell = row[index]
            ligne_list.append(cell)
        maze.append(ligne_list)
    return maze

maze = [['#', '#', '#', '#', '#', '#', '#', '#', '#', '#'], 
        ['#', 'S', '.', '_', '_', '_', '.', '#', '#', '#'], 
        ['#', '#', '#', '#', '#', '#', '#', '.', 'E', '#'], 
        ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#']]


def bfs(maze, start, end=None):  # Breadth-First Search
    queue = [start]                                 # enqueue the source node  
    visited = []                                    # list of nodes visited
    predecessor = {}                       
    while len(queue) >  0:
        node_coord = queue.pop(0)                   # remove the node from the start of the queue to process it   
        visited.append(node_coord)                  
        for n in getNeighbor(node_coord, maze):     # queue all its unexplored neighbors (at the end);
            if n not in predecessor.keys():
                queue.append(n)
                predecessor[n] = node_coord
    return visited, predecessor
    
def getNeighbor(coord, maze):
    width, heigth = len(maze[0]), len(maze)
    x, y = coord
    potential_neighbor = [(x+1, y), (x-1, y),     # right, left 
                          (x, y+1), (x, y-1),     # top, down
                          (x-1, y-1), (x-1, y+1), # top diagonal left, right
                          (x+1, y-1), (x+1, y+1)] # bottom diagonal left, right
    neighbor = [(l, c) for (l, c) in potential_neighbor if  0<=l<heigth and 0<=c<width and maze[l][c] != "#" ] 
    return neighbor

def theWayTo(end, start, p):
    route = [end]
    while end != start:
        end = p[end]
        route.append(end)
    return route[::-1]

v, p = bfs(maze, (1,1))
r = theWayTo(end=(2,8), start=(1,1), p=p)
print(" ")
print(" ")
print("visited")
print(v)
print(" ")
print("predecessor")
print(p)
print(" ")
print(" ")
print("route")
print(r)






