# sets the working directory at the level of the file's parent
import sys
from pathlib import Path
folder = Path(__file__).parent
sys.path.insert(0, str(folder))

from function import *

maze_str = '''###############
##S.........E##
##.##########.#
##._________.##
###############'''.replace('\n', "")
resp = "DL DR R UR UL"

# Shape of the maze
width  = 15
height = 5
# Transform the str maze into a list adapted to the hexagonal format
# and also returns a list of keys, gate, entry point and exit point
maze, l = mazeStrToList(maze_str = maze_str,          
                        width=width, heigth=height)
mazeToPrint =  printMaze(maze)
#Remove keyless doors and turn them into a wall
maze, l = dropDoor(letter=l, maze=maze)
atw = stepByStep(maze = maze, letter = l)
d = coordToLetter(atw)
myResp = response(direction=d)
ca = checkAnswer(resp=resp, myResp=myResp)

mazeWithRecord = recordMouvement(maze=maze, allTheWay=atw)
mazeWithRecord_str = printMaze(mazeWithRecord) 

print("="*25 + " MAZE " + "="*25); print(mazeToPrint) 
print("\n")
print("="*15 + " MAZE WITH RECORD " + "="*15); print(mazeWithRecord_str)
print("\n")
print("Le parcours");  print(d)
print("\n")
print("="*25 + " REPONSE " + "="*25); print(ca)
#print(printMaze(maze))