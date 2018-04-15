import networkx as nx
from PIL import Image
import matplotlib.pyplot as plt
import numpy
import sys
import os
import math


def inv_kinematics(x, y):
    L1 = 154.4319958
    L2 = 183.263961369
    pixel_factor = 1

    x = pixel_factor * (x + 1 + 139.7) # offset of paper
    y = pixel_factor * (width - y + 1 - 91.52171498) # offset of paper

    sqrt = math.sqrt(x**2+y**2)
    SplusQ = math.atan2(y,x)
    
    S = SplusQ - math.acos((x**2+y**2 + (L1 + L2)*(L1-L2))/(2*sqrt*L1))
    E = math.acos((x**2+y**2 - L1**2 - L2**2)/(2*L1*L2))

    return [round(math.degrees(S),4),round(math.degrees(E),4)]


def vectorize(list):
    stepslist = [[list[0][0], list[0][1]]]
    cursteplist_index = 0
    for i in range(1, len(list)):
        front = list[i][0]
        back = list[i][1]
        if list[i - 1][1] != front: # last back is not the same as current front
            cursteplist_index += 1
            stepslist.append([])
        stepslist[cursteplist_index].append(back)
    return stepslist



# 1. put image to graph of networkx
# 2. adjacent node with connected edge is up down left right upleft, upright, downleft, downright
# 3. use Minimum Spanning Tree of networkx to generate the path of filling for each region

img = Image.open("test.bmp")
im = img.convert("RGB")
G=nx.Graph()

width, height = im.size

# 2d array
matrix = []
for j in range(height):
    matrix.append([])
    for i in range(width):
        matrix[j].append(0)

# fill in matrix with 0 and 1
for x in range(width):
    for y in range(height):
        r,g,b = im.getpixel((x,y))
        # r,g,b = 0, 0, 0
        if r == 0 and g == 0 and b == 0:
            matrix[y][x] = 1
        else:
            matrix[y][x] = 0


# add nodes of the graph
for x in range(width):
    for y in range(height):
        cur_node = width * y + x
        if matrix[y][x] == 1:
            G.add_node(cur_node)

# add edges of the graph
Edges = []
for y in range(height):
    for x in range(width): 
        cur_node = width * y + x
        # up down left right
        if matrix[y][x] == 1 :
            if x % width != width - 1 and matrix[y][x+1] == 1: # Right
                Edges.append((cur_node, cur_node + 1))
            if x % width != 0 and matrix[y][x-1] == 1: # Left
                Edges.append((cur_node, cur_node - 1))
            if y < height - 1 and matrix[y+1][x] == 1: # Down
                Edges.append((cur_node, cur_node + width))
            if y > 0 and matrix[y-1][x] == 1: # Up
                Edges.append((cur_node, cur_node - width))
            # diagonal
            if x % width != width - 1 and y < height - 1 and matrix[y+1][x+1] == 1: # Down Right
                Edges.append((cur_node, cur_node + width + 1))
            if x % width != width - 1 and y > 0 and matrix[y-1][x+1] == 1: # Up Right
                Edges.append((cur_node, cur_node - width + 1))
            if x % width != 0 and y < height - 1 and matrix[y+1][x-1] == 1: # Down Left
                Edges.append((cur_node, cur_node + width - 1))
            if x % width != 0 and y > 0 and matrix[y-1][x-1] == 1: # Up Left
                Edges.append((cur_node, cur_node - width - 1))

G.add_edges_from(Edges)
subgraphs = list(nx.connected_component_subgraphs(G)) # a list of connected graphs

node_vector = []

for graph in subgraphs:
    nodes_list = list(graph.nodes())
    dsf = nx.dfs_edges(graph, nodes_list[0])
    edgelist = list(dsf)
    if len(edgelist) > 0:
        node_vector += vectorize(edgelist)

# filling node list is stored in node_vector
# print(node_vector)

#------------------------------------------------------------------------
# convert to angle
angle_vector = []
for a in node_vector:
    angle_list = []
    for element in a:

        x = int(element % width)
        y = int(element / width)

        try:
            pair = inv_kinematics(x, y)
            angle_list.append(pair)
        except:
            print("out of boundary")
            # a.remove(element)

    angle_vector.append(angle_list)

# First is shoulder, second is elbow
print(angle_vector)

vector_file= open("vector.txt","w")
for vector_item in angle_vector:
    # each list
    record = 0
    for item in vector_item:
    # each pair
        if record == 1:
            vector_file.write("down\n")
        vector_file.write("first: " + str(item[0]) + "\n")
        vector_file.write("second: " + str(item[1]) + "\n")
        record += 1
    vector_file.write("up\n")


#------------------------------------------------------------------------
# output all pictures

im = Image.new("RGB", (width, height), "white")
index = 0

if not os.path.exists('output'):
    os.makedirs('output')

for list in node_vector:
    for element in list:
        x = element % width
        y = int(element / width)
        im.putpixel((x, y), (0, 0, 0))
        path = 'output/out_' + str(index) + '.png'
        im.save(path)
        index += 1
