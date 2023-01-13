# sets the working directory at the level of the file's parent ######
import sys                                                          #
from pathlib import Path                                            #
folder = Path(__file__).parent                                      #
sys.path.insert(0, str(folder))                                     #
#####################################################################

# IMPORT
from function import *
import copy
import time

################### CHOOSE A MAZE ###################################
file = "maze11.txt"
#####################################################################

#####################################################################
########################## MAIN #####################################
#####################################################################
start = time.perf_counter()
maze, letter, resp  = getMaze(file=file) 
original_maze = copy.deepcopy(maze)        
door_wall(maze = maze, letter = letter)
atw = stepByStep(maze = maze, letter = letter)
d = coordToLetter(atw)
myResp = response(direction=d)               
ca = checkAnswer(resp=resp, myResp=myResp) 
finish = time.perf_counter()
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
print("TEMPS:", end="  "); print(f"{round(finish-start, 2)} (s)"); print("")
#####################################################################
######################## WRITTING RECORD ############################
#####################################################################
print("="*25 + " WRITTING RECORD " + "="*25); print("")
mazeWithRecord = recordMouvement(maze=original_maze, allTheWay=atw)
mazeWithRecord_str = printMaze(mazeWithRecord)
with open('Hexagonal_Maze_part2/maze/Record_'+ file + '.txt','w+') as f:
    f.write(mazeWithRecord_str)