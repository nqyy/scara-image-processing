import networkx as nx
from PIL import Image
import matplotlib.pyplot as plt
import numpy
import sys

# 1. put image to graph of networkx
# 2. adjacent node with connected edge is up down left right upleft, upright, downleft, downright
# 3. use Minimum Spanning Tree of networkx to generate the path of filling for each region

img = Image.open("out_quantize.bmp")
im = img.convert("RGB")
G=nx.Graph()

width, height = im.size
# 2d array
matrix = []
for i in range(width):
    matrix.append([])
    for j in range(height):
        matrix[i].append(0)

# fill in matrix with 0 and 1
for x in range(width):
    for y in range(height):
        r,g,b = im.getpixel((x,y))
        # r,g,b = 0, 0, 0
        if r == 0 and g == 0 and b == 0:
            matrix[x][y] = 1
        else:
            matrix[x][y] = 0

# add nodes of the graph
for x in range(width):
    for y in range(height):
        cur_node = width * y + x
        if matrix[x][y] == 1:
            G.add_node(cur_node)

# add edges of the graph
Edges = []
for y in range(height):
    for x in range(width): 
        cur_node = width * y + x
        if x % (width+1) != width - 1 and matrix[x+1][y] == 1:
            Edges.append((cur_node, cur_node + 1))
        if x % (width+1) != 0 and matrix[x-1][y] == 1:
            Edges.append((cur_node, cur_node - 1))
        if y < height - 1 and matrix[x][y+1] == 1:
            Edges.append((cur_node, cur_node + width + 1))
        if y > 0 and matrix[x][y-1] == 1:
            Edges.append((cur_node, cur_node - width - 1))

G.add_edges_from(Edges)

# show the graph
# nx.draw(G)
# plt.show()

# calculate minimum spanning edges of the graph
mst = nx.minimum_spanning_edges(G, algorithm='kruskal', data=False) # can use prim as well
edgelist=list(mst)
print(sorted(edgelist))

