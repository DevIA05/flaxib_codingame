# sets the working directory at the level of the file's parent
import sys
from pathlib import Path
folder = Path(__file__).parent
sys.path.insert(0, str(folder))

from function import *

maze_str = '''##########
#S.#######
###.######
###.######
###..#####
##.#.#####
##a##A####
##.##.####
###..B..E#
##########'''.replace('\n', "")
resp = "R DR DR DL DL DL UR UR R DR DR DR DR R R"

# Shape of the maze
width  = 10
height = 10
# Transform the str maze into a list adapted to the hexagonal format
# and also returns a list of keys, gate, entry point and exit point
maze, l = mazeStrToList(maze_str = maze_str,          
                        width=width, heigth=height)
# Remove keyless doors and turn them into a wall
maze, l = dropDoor(letter=l, maze=maze)
atw = stepByStep(maze = maze, letter = l)
d = coordToLetter(atw)
myResp = response(direction=d)
ca = checkAnswer(resp=resp, myResp=myResp)

mazeWithRecord = recordMouvement(maze=maze, allTheWay=atw)
mazeWithRecord_str = printMaze(mazeWithRecord) 

print(" ")
print("="*25 + " MAZE " + "="*25); print(mazeWithRecord_str)
print("\n")
print("Le parcours");  print(d)
print("\n")
print("="*25 + " REPONSE " + "="*25); print(ca)
