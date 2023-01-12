import sys
import math
import time
import re
import copy

# Coding Game -> comment line 15,16, 22, 33, 34

#** Transform the string maze into a list, and retrieves the coordinates of each letter
#** return tuple[list[list[str]], dict[str, tuple[int, int]]] 
def getMaze(file):
    #width, height = [int(i) for i in input().split()]; 
    f = open("Hexagonal_Maze_part2/maze/" + file, "r")              # Open the connection with the file.
    sh = f.readline()[:-1];                                         # Get the first line to extract the dimensions of the labyrinth.
    lsh = sh.split(" "); width = int(lsh[0]); height = int(lsh[1])  # Extract dimension and cast to int. 
    width = width * 2                                               # We multiply the width by two to correspond to the hexagonal format of the labyrinth.                                                       
    letter = {}                                                     # Will contain the keys, the doors, the start point and arrival as well as their respective. 
                                                                    #    coordinates in the object which will contain the labyrinth.
    maze = []                                                       # Contains the elements composing the labyrinth each character of a line of the file will 
                                                                    #    be in a list which will then be added to maze.
    for h in range(0, height):                                      # For each line of the labyrinth:       
        ligne = ["#"]*width                                           # Here it is purely aesthetic, instead of adding after or before the character "0",
                                                                      #    we will put it only when it is surrounded by space to move.
        row = f.readline()[:-1] #input()                              # We retrieve the line without taking the character '\n' ([:-1]).
        if(h%2 ==0): s = 0; hexa = 1                                  # s corresponds to the value from which we will move in line list to add the characters, 
        else: s = 1; hexa = -1                                        #    this will allow us to apply a shift every other line of the table containing the labyrinth.
                                                                      #    s = 0, we will have a shift to the right
                                                                      #    s = 1, we will have a shift to the left
                                                                      # hexa with w makes it possible to find the index allowing to move in the line to recover the 
                                                                      #    current character.
        
        for w in range(s, width, 2):                                  # Go through in steps of two to leave a box for the character "0" (as a reminder, we doubled the width)
            index = int((w+hexa)/2)                                   # Find the index allowing to move in row (containing the characters of the current line). 
                                                                      #    cast to int to recover the integer part if we start with 0, int((0+1)/2) = int(0.5) = 0
            ligne[w] = row[index]                                     # Add current character to the list.     
            saveLetter(n = (h, w), ch = row[index], letter = letter)         
            if(index+hexa not in [-1, width/2]):                      # Test if we do not leave the range, if we start at 0, we do not need to check the character at position 
                                                                      #    -1 and if we are at the end we have no character at the position beyond the end.
                if(row[index]!= "#" and row[index+hexa]!="#"):        # I add it if before or after there is no # character, (if a displacement character is not at side of a wall)
                    ligne[w+hexa] = "0"
        maze.append(ligne)                                            # Add the list containing the characters of the line to maze
    resp = f.readline(); f.close()                                  # Retrieve the expected response then I close the connection with the file.
    return maze, letter, resp
    #return maze, letter

#** Breadth-First Search 
#** we retrieve the neighbors of all box that are not walls
#** maze{list[list[str]]]} represents the labyrinth
#** start{tuple[int, int]}: starting point coordinates
# ** return list[tuple[int, int]] and dict{tuple[int, int], tuple[int, int]}
def bfs(maze, start):
    queue = [start]                                 # enqueue the source node  
    visited = []                                    # list of nodes visited
    predecessors = {}                               # key: tuple[int, int], value: tuple[int, int]                     
    val = 0
    while len(queue) >  0:
        node_coord = queue.pop(0)                   # remove the node from the start of the queue to process it   
        visited.append(node_coord)                 
        for n in getNeighbor(node_coord, maze):     # queue all its unexplored neighbors (at the end);
            if n not in predecessors.keys():        # n: tuple[int, int] coordinate of neightbor
                queue.append(n)
                predecessors[n] = node_coord               
    return(visited, predecessors)

#** Saves the coordinates and the name of the keys and door
#** n: tuple[int, int]
#** ch: str
#** letter: dict
#** return dict[str, list[tuple[int, int]]]
def saveLetter(n, ch, letter):  
    if(ch.isalpha()):
        if(ch in letter.keys()): letter[ch].append(n) # if there is the same door at different coordinates
        else: letter[ch] = [n]
    return letter

#** Get neighboring node
#** Get coordinate neighboring node and keep those who are not walls
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
#** p: tuple[int, int] predecessor coordinate of sliding floor
#** sf: tuple[int, int] sliding floor coordinate
#** maze: list[list[str]]
#** return: tuple[int, int] coordinate terminus
def getTerminus(p, sf, maze):
    gradient = sf[0]-p[0], sf[1]-p[1]               # determines the slope from the two points 
                                                    #   Δx = x2 - x1
                                                    #   Δy = y2 - y1
    nextNode = sf[0]+gradient[0], sf[1]+gradient[1] # get the next node coordinate in the same direction
    stop = False                                    # while loop stop condition
    while stop == False:
        node = maze[nextNode[0]][nextNode[1]]
        if node == '#':                                                    # if the next vertex is a wall or a door then:
            nextNode = nextNode[0]-gradient[0], nextNode[1]-gradient[1]    #    we come back to the previous node
            stop = True;
        elif node == '.' or node == 'E':
            stop = True
        else: nextNode = nextNode[0]+gradient[0], nextNode[1]+gradient[1]
    return nextNode

#** Get route from start to end
#** trace the predecessors back to source
#** end  : tuple[int, int]    arrival point coordinates
#** start: tuple[int, int]    starting point coordinates
#** p    : dict[tuple, tuple] predecessors of each node
#** return list sorted from the start
def theWayTo(end, start, p ):
    route = [end]
    # trace the predecessors back to source
    while end != start:
        end = p[end]
        route.append(end)
    return route[::-1] # reverse the list, the list contains the points from the end 
                       #   to the beginning

# Turn doors into walls
def door_wall(maze, letter): # list[list[str]], dict[str, tuple[int, int]] -> list[list[str]]
    doors = [k for k in letter.keys() if(k.isupper() and k not in ['S', 'E'])]
    for d in doors:
        for x, y in letter[d]:
            maze[x][y] = '#'

# Turns doors into free space
def door_freeSpace(maze, door): # list[list[str]], list[tuple[int, int]]  
    for dx, dy in door:
        maze[dx][dy] = "."    

#** Performs breadth-first search on the different elements of the labyrinth
#** I get the predecessors from breadth-first search.
#** The doors being walls, if we need a key we go to recover it by going back 
#** to the predecessors.
#** then we transform the door corresponding to the key into an free space 
def stepByStep(maze, letter): # list[list[tuple(int, int)]], dict[str, tuple[int, int]] -> list[tuple[int, int]]
    allTheWay: list[tuple[int, int]] = []
    keyring: list[str] = ['S'] + sorted([k for k in letter.keys() if k.islower()]) + ["E"]
    maze[letter['S'][0][0]][letter['S'][0][1]] = "."
    for i in range(0, len(keyring[:-1])):
        s = letter[keyring[i]][0]; e = letter[keyring[i+1]][0]
        v, p = bfs(maze, start = s)                          # I get the predecessors from breadth-first search
        if(letter['E'][0] not in p.keys()):                  # if can't we already access the exit 
            r = theWayTo(end=e, start=s, p=p)[:-1]              # the doors being walls, if we need a key we go to recover 
                                                                #   it by going back to the predecessors.
                                                                #   we do not take the last value which is the end point 
            allTheWay += r  
            door_freeSpace(maze, letter[keyring[i+1].upper()])     # we transform the door corresponding to the key into an free space 
        else:                                                # if we can already access the exit
            r = theWayTo(end=letter['E'][0], start=s, p=p)
            allTheWay += r
            break;
    return allTheWay

#** Convert path from coordinate to direction
#** route: list[tuple[int, int]]) 
#** return list[str] 
def coordToLetter(route):
    sign = lambda x: (x>0) - (x<0) # will determine the direction based on the sign of x and y
    directions = []    
    for c in range(0, len(route[:-1])):
        x, y = route[c+1][0]-route[c][0], route[c+1][1]-route[c][1]
        if   sign(x) == -1 and sign(y) ==  1 : directions.append("UR")
        elif sign(x) == -1 and sign(y) == -1 : directions.append("UL")
        elif sign(x) ==  1 and sign(y) == -1 : directions.append("DL")
        elif sign(x) ==  1 and sign(y) ==  1 : directions.append("DR")
        elif sign(x) ==  0 and sign(y) ==  1 : directions.append("R")
        elif sign(x) ==  0 and sign(y) == -1 : directions.append("L")
        else: directions.append(f"Erreur coordToLetter, iteration: {c}")
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

#** Each step is represented by a number
def recordMouvement(maze, allTheWay):
    i = 0
    mazeWithRecord = copy.deepcopy(maze)
    for x, y in allTheWay:
        i += 1
        if(bool(re.search(r'\d', mazeWithRecord[x][y]))): mazeWithRecord[x][y] = mazeWithRecord[x][y] + "," + str(i)  
        else: mazeWithRecord[x][y] = str(i)
    return mazeWithRecord

#** Concatenate directions from list direction to have a str
def response(direction): # list[str] -> str
    return ' '.join(direction)

#** Checks if the found answer matches the expected answer
def checkAnswer(resp, myResp): # str, str -> Boolean
    return resp == myResp
