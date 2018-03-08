import networkx as nx
from PIL import Image

# 1. put image to graph of networkx
# 2. adjacent node with connected edge is up down left right upleft, upright, downleft, downright
# 3. use Minimum Spanning Tree of networkx to generate the path of filling for each region

im = Image.open("out_quantize.bmp")
#TODO

