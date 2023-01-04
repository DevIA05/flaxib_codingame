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

#** Breadth-First Search
#** maze{liste 2D} represents the labyrinth
#** start{tuple} starting point coordinates
def bfs(maze, start):  # Breadth-First Search
    queue = [start]                                 # enqueue the source node  
    visited = []                                    # list of nodes visited
    predecessors = {}                       
    while len(queue) >  0:
        node_coord = queue.pop(0)                   # remove the node from the start of the queue to process it   
        visited.append(node_coord)                  
        for n in getNeighbor(node_coord, maze):     # queue all its unexplored neighbors (at the end);
            if n not in predecessors.keys():
                queue.append(n)
                predecessors[n] = node_coord
    return visited, predecessors
    
def getNeighbor(coord, maze):
    width, heigth = len(maze[0]), len(maze)
    x, y = coord                                  # x: line, y: column
    potential_neighbor = [(x+1, y), (x-1, y),     # right, left 
                          (x, y+1), (x, y-1),     # top, down
                          (x-1, y-1), (x-1, y+1), # top diagonal left, right
                          (x+1, y-1), (x+1, y+1)] # bottom diagonal left, right
    #neighbor = [(l, c) for (l, c) in potential_neighbor if  0<=l<heigth and 0<=c<width and maze[l][c] != "#" ] 
    neighbor = []
    for (l, c) in potential_neighbor:
        if 0<=l<heigth and 0<=c<width and maze[l][c] != "#":
            if(maze[l][c]=="_"): neighbor.append(
                                   getTerminus(p=coord, sf=(l,c), maze=maze))
            else: neighbor.append((l,c))
    return neighbor

#** At the end of the sliding floor
#** get the coordinates of the last point (terminus) of the sliding floor
#** p{tuple} predecessor coordinate
#** sf{tuple} sliding floor coordinate
def getTerminus(p, sf, maze):
    gradient = sf[0]-p[0], sf[1]-p[1]               # determines the slope from the two points 
                                                    #   Δx = x2 - x1
                                                    #   Δy = y2 - y1
    nextNode = sf[0]+gradient[0], sf[1]+gradient[1] # get the next node coordinate in the same direction
    stop = False                                                        # while loop stop condition
    while stop == False:
        if maze[nextNode[0]][nextNode[1]] == "#":                       # if the next vertex is a wall then:
            nextNode = nextNode[0]-gradient[0], nextNode[1]-gradient[1] # we come back to the previous node
            stop = True;
        elif maze[nextNode[0]][nextNode[1]] == ".":         
            stop = True
        else: nextNode = nextNode[0]+gradient[0], nextNode[1]+gradient[1]
    return nextNode

#** Get route from start to end
#** trace the predecessors back to source
#** end{tuple} arrival point coordinates
#** start{tuple} starting point coordinates
#** p{dict} predecessors of each node
#** return {list} list sorted from the start 
#**               point to the end point including the imprinted nodes 
def theWayTo(end, start, p):
    route = [end]
    while end != start:
        end = p[end]
        route.append(end)
    return route[::-1]        # reverse the list

#** Dsiplay the maze with coordinates
#** maze{list 2D} 
def printMaze(maze):
    print("    0    1    2    3    4    5    6    7    8    9")
    for i in range(0, len(maze)): print(f"{i} {maze[i]}")