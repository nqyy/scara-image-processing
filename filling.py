import networkx as nx
from PIL import Image
import matplotlib.pyplot as plt
import numpy
import sys
import os



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

img = Image.open("out_quantize.bmp")
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
            if x % width != width - 1 and matrix[y][x+1] == 1: # 右
                Edges.append((cur_node, cur_node + 1))
            if x % width != 0 and matrix[y][x-1] == 1: # 左
                Edges.append((cur_node, cur_node - 1))
            if y < height - 1 and matrix[y+1][x] == 1: # 下
                Edges.append((cur_node, cur_node + width))
            if y > 0 and matrix[y-1][x] == 1: # 上
                Edges.append((cur_node, cur_node - width))
            # diagonal
            if x % width != width - 1 and y < height - 1 and matrix[y+1][x+1] == 1: # 右下
                Edges.append((cur_node, cur_node + width + 1))
            if x % width != width - 1 and y > 0 and matrix[y-1][x+1] == 1: # 右上
                Edges.append((cur_node, cur_node - width + 1))
            if x % width != 0 and y < height - 1 and matrix[y+1][x-1] == 1: # 左下
                Edges.append((cur_node, cur_node + width - 1))
            if x % width != 0 and y > 0 and matrix[y-1][x-1] == 1: # 左上
                Edges.append((cur_node, cur_node - width - 1))

G.add_edges_from(Edges)
subgraphs = list(nx.connected_component_subgraphs(G)) # a list of connected graphs

# calculate minimum spanning edges of the graph
# mst = nx.minimum_spanning_edges(G, algorithm='kruskal', data=False) # can use prim as well

node_vector = []

for graph in subgraphs:
    nodes_list = list(graph.nodes())
    dsf = nx.dfs_edges(graph, nodes_list[0])
    edgelist = list(dsf)
    if len(edgelist) > 0:
        node_vector += vectorize(edgelist)
    
# print(node_vector)
# filling node list is stored in node_vector

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
