# sets the working directory at the level of the file's parent
import sys
from pathlib import Path
folder = Path(__file__).parent
sys.path.insert(0, str(folder))

from function import *
import copy

maze_str = '''##########
#S.___.###
#######.E#
##########'''.replace('\n', "")
resp = "R R DR R"

# Shape of the maze
width  = 10 
height = 4  
# Transform the str maze into a list adapted to the hexagonal format
# and also returns a list of keys, gate, entry point and exit point
maze, l = mazeStrToList(maze_str = maze_str,          
                        width=width, heigth=height)
#Remove keyless doors and turn them into a wall
mazewithoutDoor = door_wall(maze = maze, letter = l)
atw = stepByStep(maze = mazewithoutDoor, letter = l)
d = coordToLetter(atw)
myResp = response(direction=d)
ca = checkAnswer(resp=resp, myResp=myResp)
mazeWithRecord = recordMouvement(maze=maze, allTheWay=atw)
mazeWithRecord_str = printMaze(mazeWithRecord)


print("="*25 + " MAZE " + "="*25); 
print(printMaze(maze)); print(" ")
#print(mwdPrint); print("\n")
print("="*15 + " MAZE WITH RECORD " + "="*15); print(mazeWithRecord_str)
print("\n")
print("="*25 + " RESULT " + "="*25); print("")
print("Le parcours"); 
for i in range(0, len(d)): print(f"{i+1}: {d[i]}", end="; ")
print("\n")
print("Bonne réponse"); print(resp);
print("")
print("Réussite: ", end=""); print(ca); print("")

# print ("="*25 + "BROUILLON" + "="*25)
# mazeWithoutDoor = door_wall(maze= maze, letter= l)
# mwd_str = printMaze(mazeWithoutDoor)
# print(mwd_str)
with open('Hexagonal_Maze_part2/maze/maze10.txt','w+') as f:
    f.write(printMaze(maze))
with open('Hexagonal_Maze_part2/maze/Record_maze10.txt','w+') as f:
    f.write(mazeWithRecord_str)