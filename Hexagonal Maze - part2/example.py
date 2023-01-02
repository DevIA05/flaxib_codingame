
# import sys
# import math

# class node:
#     def __init__(self, valeur, position, voisinage):
#         self.val       = valeur
#         self.pos       = position
#         self.voisinage = voisinage 


# node_list  = []
# maze_list  = []

# # Auto-generated code below aims at helping you parse
# # the standard input according to the problem statement.
# w, h = [int(i) for i in input().split()]
# #print(w, file=sys.stderr, flush=True)
# for ligne in range(h):
#     row = input()
#     ligne_list = []
#     for index in range(0, len(row)):
#         cell = row[index]
#         ligne_list.append(cell)
#     maze_list.append(ligne_list)



# for l in range(0, len(maze_list)):
#     for i in range(0, len(maze_list[l])):
#         cell = maze_list[l][i]
#         if(cell != "#"):
#             pass

# def getNeighbor(l, i, maze_list):
#     list_neighbor = []
#     # voisinage en haut 
#     if(l > 0):
#         list_neighbor.append(maze_list[l-1][i])
#     # voisinage en bas 
#     if(l < len(maze_list)-1):
#         list_neighbor.append(maze_list[l+1][i])
#     # à gauche
#     if(i > 0):
#         list_neighbor.append(maze_list[l][i-1])
#     # à droite
#     if(i < len(maze_list[l])-1):
#         list_neighbor.append(maze_list[l][i+1])
#         list_neighbor.append(maze_list[l+1][i+1])
#     return list_neighbor
        


import sys
import math

node_list  = []
maze_list  = []
#padding_ch = "#"

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.
w, h = [int(i) for i in input().split()]
for ligne in range(h):
    row = input()
    print(row, file=sys.stderr, flush=True)
    ligne_list = []
    for index in range(0, len(row)):
        cell = row[index]
        ligne_list.append(cell)
    maze_list.append(ligne_list)


def getNeighbor(coord, maze_list):
    x, y = coord
    list_neighbor = [(x+1, y), (x-1, y), 
                     (x, y+1), (x, y-1)]

    #return list_neighbor
        




# Write an answer using print
# To debug: print("Debug messages...", file=sys.stderr, flush=True)




# Write an answer using print
# To debug: print("Debug messages...", file=sys.stderr, flush=True)

