# sets the working directory at the level of the file's parent ######
import sys                                                          #
from pathlib import Path                                            #
folder = Path(__file__).parent                                      #
sys.path.insert(0, str(folder))                                     #
#####################################################################

from function import *
import copy

# pick up the labyrinth to go through it
file = "maze11.txt"

#####################################################################
########################## MAIN #####################################
#####################################################################
# Transform the str maze into a list adapted to the hexagonal format
# and also returns a list of keys, gate, entry point and exit point
maze, letter, resp  = getMaze(file=file)
original_maze = copy.deepcopy(maze) # comment in coding game
door_wall(maze = maze, letter = letter)
atw = stepByStep(maze = maze, letter = letter)
d = coordToLetter(atw)
myResp = response(direction=d)
ca = checkAnswer(resp=resp, myResp=myResp)

#####################################################################
######################### PRINT RESULT ##############################
#####################################################################
print("="*25 + " RESULT " + "="*25); print("")
print("Le parcours"); 
for i in range(0, len(d)): print(f"{i+1}: {d[i]}", end="; ")
print("\n")
print("Bonne réponse"); print(resp);
print("")
print("Réussite: ", end=""); print(ca); print("")

#####################################################################
######################## WRITTING RECORD ############################
#####################################################################
print("="*25 + " WRITTING RECORD " + "="*25); print("")
mazeWithRecord = recordMouvement(maze=original_maze, allTheWay=atw)
mazeWithRecord_str = printMaze(mazeWithRecord)
with open('Hexagonal_Maze_part2/maze/Record_'+ file + '.txt','w+') as f:
    f.write(mazeWithRecord_str)