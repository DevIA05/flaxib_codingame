import sys
import math
import time
import re
import copy

# def function(arg1: str, arg2: str) -> list:
#     args = [arg1, arg2]
#     return args

def mazeStrToList(maze_str:str, width:int, heigth:int):
    maze_list: list = []  # will contain the elements composing the maze taking into account the hexagonal aspect
    count:     int  = 0   # browse the elements in maze_str
    ligne:     list = []  # will contain the elements on a length of width taking into account the hexagonal aspect
    letter:    dict[str, tuple[int,int]] = {}  # stores entry, exit, keys and doors 
    for h in range(0, heigth):
        for w in range(0, width):
            if(h%2 == 0): 
                if(w == width-1): ligne.extend([maze_str[count], "#"]);
                else:
                    if(maze_str[count] == "#" or maze_str[count+1] == "#"): ligne.extend([maze_str[count], "#"]); 
                    else: ligne.extend([maze_str[count], "0"]);
                W = w*2      # position in the horizontal axis in maze_list
            else:
                if(w==0): ligne.extend(['#', maze_str[count]]);
                else:
                    if(maze_str[count] == "#" or maze_str[count-1] == "#" ): ligne.extend(["#", maze_str[count]]);
                    else: ligne.extend(['0', maze_str[count]]);
                W = (w*2)+1  # position in the horizontal axis in maze_list
            letter = saveLetter(n=(h,W), ch=maze_str[count], letter=letter)
            count += 1 # moves to the next element in the maze_str object
        maze_list.append(ligne)
        ligne = []
    return maze_list, letter

#** Breadth-First Search 
#** we retrieve the neighbors of all box that are not walls
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
        if(ch in letter.keys()): letter[ch].append(n) # if there is the same door at different coordinates
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
    stop = False                                    # while loop stop condition
    while stop == False:
        node = maze[nextNode[0]][nextNode[1]]
        if node == '#' or (node.isupper() and node != 'E'):                                    # if the next vertex is a wall or a door then:
            nextNode = nextNode[0]-gradient[0], nextNode[1]-gradient[1]    #    we come back to the previous node
            stop = True;
        elif node == '.' or node.islower() or node == 'E':
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

#** Removes keyless doors and replaces them with walls
#** letter{dict[str, tuple[int, int]]}
#** maze{list[list[str]]} 
def dropDoor(maze, letter):  
    for d in list(letter.keys()): #  use list to force a copy of the keys to thus remove a key from the dictionary 
                                  #  without the iteration being impacted
        if(d not in ["S", "E"]):
            if(d.isupper() and d.lower() not in letter.keys()):
                x, y = letter[d][0][0], letter[d][0][1]
                maze[x][y] = "#"
                del letter[d]
    return maze, letter

# Turn doors into walls
def door_wall(maze, letter): # list[list[str]], dict[str, tuple[int, int]] -> list[list[str]]
    newMaze = copy.deepcopy(maze)
    doors = [k for k in letter.keys() if(k.isupper() and k not in ['S', 'E'])]
    for d in doors:
        for x, y in letter[d]:
            newMaze[x][y] = '#'
    return newMaze

def open_door(maze, keyring):
    pass
    
    

#** Performs the path in width from the starting point to the first key, 
#** from key c to the corresponding door, and ends with the path from the door 
#** to the end point
def stepByStep(maze, letter): # list[list[tuple(int, int)]], dict[str, tuple[int, int]] -> list[tuple[int, int]]
    allTheWay = []
    keys = ['S'] + sorted([k for k in letter.keys() if k.islower()]) + ["E"]
    for i in range(0, len(keys[:-1])):
        s = letter[keys[i]][0]; e = letter[keys[i+1]][0]
        v, p = bfs(maze, start = s)
        if(letter['E'][0] not in p.keys()):                # if can't we already access the exit 
            r = theWayTo(end=e, start=s, p=p)[:-1]         # we do not take the last value which is the end point 
            allTheWay += r
            dx, dy = letter[keys[i+1].upper()][0]
            maze[dx][dy] = "."
        else:                                              # if we can already access the exit
            r = theWayTo(end=letter['E'][0], start=s, p=p)
            allTheWay += r
            break;
    return allTheWay

#** Convert path from coordinate to direction
# ** route{list[tuple[int, int]]}
def coordToLetter(route): # -> list[str]
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
    maze_str = ""
    ligne = 0
    l1 = ["  "+str(n) if n <= 10 else " "+str(n) for n in range(0, len(maze[0]))]
    maze_str += "" + ''.join(l1) + "\n"
    for l in maze:
        l_str = '  '.join(l)
        maze_str += str(ligne) + " " + l_str + "\n"
        ligne += 1
    return maze_str

def recordMouvement(maze, allTheWay):
    i = 0
    mazeWithRecord = copy.deepcopy(maze)
    for x, y in allTheWay:
        i += 1
        if(bool(re.search(r'\d', mazeWithRecord[x][y]))): mazeWithRecord[x][y] = mazeWithRecord[x][y] + "," + str(i)  
        else: mazeWithRecord[x][y] = str(i)
    return mazeWithRecord

# Concatenate directions from list direction to have a str
def response(direction): # list[str] -> str
    return ' '.join(direction)

def checkAnswer(resp, myResp): # str, str -> Boolean
    return resp == myResp
