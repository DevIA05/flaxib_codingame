# sets the working directory at the level of the file's parent
import sys
from pathlib import Path
folder = Path(__file__).parent
sys.path.insert(0, str(folder))

from function import *

maze_str = '''########
#S.#####
##.__A##
##a##.E#'''.replace('\n', "")

width  = 8
height = 4
maze, l = mazeStrToList(maze_str = maze_str, 
                        width=width, heigth=height)
v, p = bfs(maze = maze, start = l["S"][0])
# r = theWayTo(end=(2,8), start=(1,1), p=p)
# d = coordToLetter(r)

print(" ")
print("="*25 + " MAZE " + "="*25); printMaze(maze)
print("\n")
print("visited"); print(v)
print(" ")
print("predecessor"); print(p)
print(" ")
print("letter"); print(l)
# print("\n")
# print("route"); print(r)
# print("\n")
# print("directions"); print(d)
# #print("terminus"); print(getTerminus((1,2), (1,3), maze))
