import sys
import math

# def function(arg1: str, arg2: str) -> list:
#     args = [arg1, arg2]
#     return args

def mazeStrToList(maze_str:str, width:int, heigth:int):
    maze_list: list = []
    count:     int  = 0
    ligne:     list = []
    letter:    dict[str, tuple[int,int]] = {} 
    for h in range(0, heigth):
        for w in range(0, width):
            if(h%2 == 0): ligne.extend([maze_str[count], "0"]);
            else: ligne.extend(['0', maze_str[count]]);
            letter = saveLetter(n=(h,w), ch=maze_str[count], letter=letter)
            count += 1
        if(h%2==0): ligne[(width*2)-1]="#"
        else: ligne[0]="#"
        maze_list.append(ligne)
        ligne = []
    return maze_list, letter
    # Si impair alors ajoute en second et avant dernier '#'        

#** Breadth-First Search
#** maze{liste 2D} represents the labyrinth
#** start{tuple[int, int]} starting point coordinates
def bfs(maze, start):  # Breadth-First Search
    queue = [start]                                 # enqueue the source node  
    visited = []                                    # list of nodes visited
    predecessors = {}                               # key: tuple[int, int], value: tuple[int, int]                     
    while len(queue) >  0:
        node_coord = queue.pop(0)                   # remove the node from the start of the queue to process it   
        visited.append(node_coord)                  
        for n in getNeighbor(node_coord, maze):     # queue all its unexplored neighbors (at the end);
            if n not in predecessors.keys():        # n: tuple[int, int] coordinate of neightbor
                queue.append(n)
                predecessors[n] = node_coord               
    return visited, predecessors

#** Saves the coordinates and the name of the keys and door
#** n: tuple[int, int]
#** ch: str
#** letter: dict
#** return dict[str, tuple[int, int]]:  
def saveLetter(n, ch, letter):  
    if(ch.isalpha()):
        if(ch in letter.keys()): letter[ch].append(n)
        else: letter[ch] = [n]
    return letter
    

def getNeighbor(coord, maze):
    width, heigth = len(maze[0]), len(maze)
    x, y = coord          # x: line, y: column  
    potential_neighbor = [#(x+1, y), (x-1, y),     # bottom, top
                          #(x, y+1), (x, y-1),     # right, left
                          (x, y+2) if maze[x][y+1]=="0" else (x, y+1), # right
                          (x, y-2) if maze[x][y-1]=="0" else (x, y-1), # left                         
                          (x-1, y-1), (x-1, y+1),                      # diagonal top left, right
                          (x+1, y-1), (x+1, y+1)]                      # diagonal bottom left, right
    neighbor = []
    for (l, c) in potential_neighbor:
        if 0<=l<heigth and 0<=c<width and maze[l][c] != "#":
            if(maze[l][c]=="_"): neighbor.append(
                                   getTerminus(p=coord, sf=(l,c), maze=maze))
            else: neighbor.append((l,c))
    return neighbor

#** At the end of the sliding floor
#** get the coordinates of the last point (terminus) of the sliding floor
#** p{tuple[int, int]} predecessor coordinate
#** sf{tuple[int, int]} sliding floor coordinate
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
#** end{tuple[int, int]} arrival point coordinates
#** start{tuple[int, int]} starting point coordinates
#** p{dict[key: tuple, value: tuple]} predecessors of each node
#** return {list[tuple[int, int]]} list sorted from the start 
#**               point to the end point including the imprinted nodes 
def theWayTo(end, start, p):
    route = [end]
    while end != start:
        end = p[end]
        route.append(end)
    return route[::-1]        # reverse the list

#** Convert path from coordinate to direction
# ** route{list[tuple[int, int]]}
def coordToLetter(route):
    sign = lambda x: (x>0) - (x<0)
    directions = []    
    for c in range(0, len(route[:-1])):
        x, y = route[c+1][0]-route[c][0], route[c+1][1]-route[c][1]
        if   sign(x) == -1 and sign(y) ==  1 : directions.append("UR")
        elif sign(x) == -1 and sign(y) == -1 : directions.append("UL")
        elif sign(x) ==  1 and sign(y) == -1 : directions.append("DL")
        elif sign(x) ==  1 and sign(y) ==  1 : directions.append("DR")
        elif sign(x) ==  0 and sign(y) ==  1 : directions.append("R")
        elif sign(x) ==  0 and sign(y) == -1 : directions.append("L")
        else: return(print(f"Erreur coordToLetter, iteration: {c}"))
    return directions

#** Dsiplay the maze with coordinates
#** maze{list 2D} 
def printMaze(maze):
    l1 = ""
    for n in range(0, len(maze[0])): 
        if(n<=10): l1 += f"    {n}"
        else: l1 += f"  {n} " 
    print(l1)
    for i in range(0, len(maze)): print(f"{i} {maze[i]}")