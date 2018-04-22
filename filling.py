import math
import os
import sys

import networkx as nx
from PIL import Image


def inv_kinematics(x, y, L1, L2, pixel_factor):
    # L1 back arm, L2 front arm.

    x = pixel_factor * (x + 1) - width / 2  # offset of paper
    y = pixel_factor * (320 - y + 1)  # offset of paper
    # guarentee a 200 mm x 145 mm image

    sqrt = math.sqrt(x**2 + y**2)
    SplusQ = math.atan2(y, x)

    S = SplusQ - math.acos((x**2 + y**2 + (L1 + L2) *
                            (L1 - L2)) / (2 * sqrt * L1))
    E = math.acos((x**2 + y**2 - L1**2 - L2**2) / (2 * L1 * L2))

    return [round(math.degrees(S), 6), round(math.degrees(S + E), 6)]


def vectorize(list):
    stepslist = [[list[0][0], list[0][1]]]
    cursteplist_index = 0
    for i in range(1, len(list)):
        front = list[i][0]
        back = list[i][1]
        if list[i - 1][1] != front:  # last back is not the same as current front
            cursteplist_index += 1
            stepslist.append([])
        stepslist[cursteplist_index].append(back)
    return stepslist


#====================================================================================
# 1. put image to graph of networkx
# 2. adjacent node with connected edge is up down left right upleft, upright, downleft, downright
# 3. use DFS of networkx to generate the path of filling for each region
# 4. transfer the path to angles

# get configuration from config file
try:
    s = open("configuration.config", "r")
except:
    sys.exit("File 'quantize.config' is missing")

settings = s.readlines()
i = 0
for line in settings:
    settings[i] = line[line.index(":") + 2: -1]
    i += 1

L1 = float(settings[4])
L2 = float(settings[5])
pixel_factor = float(settings[6])
animation = settings[7]

#------------------------------------------------------------------------
img = Image.open("out_quantize.bmp")
im = img.convert("RGB")

colors = im.getcolors()
picture_colors = []
for item in colors:
    picture_colors.append(item[1])

# remove white
try:
    picture_colors.remove((252, 252, 252))
except:
    pass

width, height = im.size

node_vectors = []  # holding node vectors for each color
for z in range(len(picture_colors)):
    matrix = []
    for j in range(height):
        matrix.append([])
        for i in range(width):
            matrix[j].append(0)

    # fill in matrix with 0 and 1
    for x in range(width):
        for y in range(height):
            r, g, b = im.getpixel((x, y))
            # r,g,b = 0, 0, 0
            if r == picture_colors[z][0] and g == picture_colors[z][1] and b == picture_colors[z][2]:
                matrix[y][x] = 1
            else:
                matrix[y][x] = 0

    G = nx.Graph()
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
            if matrix[y][x] == 1:
                if x % width != width - 1 and matrix[y][x + 1] == 1:  # Right
                    Edges.append((cur_node, cur_node + 1))
                if x % width != 0 and matrix[y][x - 1] == 1:  # Left
                    Edges.append((cur_node, cur_node - 1))
                if y < height - 1 and matrix[y + 1][x] == 1:  # Down
                    Edges.append((cur_node, cur_node + width))
                if y > 0 and matrix[y - 1][x] == 1:  # Up
                    Edges.append((cur_node, cur_node - width))
                # diagonal
                # Down Right
                if x % width != width - 1 and y < height - 1 and matrix[y + 1][x + 1] == 1:
                    Edges.append((cur_node, cur_node + width + 1))
                # Up Right
                if x % width != width - 1 and y > 0 and matrix[y - 1][x + 1] == 1:
                    Edges.append((cur_node, cur_node - width + 1))
                # Down Left
                if x % width != 0 and y < height - 1 and matrix[y + 1][x - 1] == 1:
                    Edges.append((cur_node, cur_node + width - 1))
                # Up Left
                if x % width != 0 and y > 0 and matrix[y - 1][x - 1] == 1:
                    Edges.append((cur_node, cur_node - width - 1))

    G.add_edges_from(Edges)
    subgraphs = list(nx.connected_component_subgraphs(G)
                     )  # a list of connected graphs

    node_vector = []

    for graph in subgraphs:
        nodes_list = list(graph.nodes())
        dsf = nx.dfs_edges(graph, nodes_list[0])
        edgelist = list(dsf)
        if len(edgelist) > 0:
            node_vector += vectorize(edgelist)
        # filling node list is stored in node_vector
    node_vectors.append(node_vector)
# node_vectors contains different color

#------------------------------------------------------------------------
# optimization

node_to_remove = []
opt_node_vectors = node_vectors
# print(opt_node_vectors)

for opt_node_vector in opt_node_vectors:
    for item in opt_node_vector:
        for i in range(len(item)):
            # updown, leftright, leftup to downright, rightup to downleft
            # up <-> down
            if i > 0 and i < len(item) - 1 and item[i] == item[i - 1] + width and item[i] == item[i + 1] - width:
                node_to_remove.append(item[i])
            elif i > 0 and i < len(item) - 1 and item[i] == item[i - 1] - width and item[i] == item[i + 1] + width:
                node_to_remove.append(item[i])

            # left <-> right (i not leftmost not rightmost)
            elif (i > 0 and i < len(item) - 1 and
                    item[i] % width != 0 and item[i] % width != width - 1 and
                    item[i] == item[i - 1] + 1 and item[i] == item[i + 1] - 1):
                node_to_remove.append(item[i])
            elif (i > 0 and i < len(item) - 1 and
                    item[i] % width != 0 and item[i] % width != width - 1 and
                    item[i] == item[i - 1] - 1 and item[i] == item[i + 1] + 1):
                node_to_remove.append(item[i])

            # left up <-> right down
            elif (i > 0 and i < len(item) - 1 and
                    item[i] % width != 0 and item[i] % width != width - 1 and
                    int(item[i] / width) != 0 and int(item[i] / width) != height - 1 and
                    item[i] == item[i - 1] + width + 1 and item[i] == item[i + 1] - width - 1):
                node_to_remove.append(item[i])
            elif (i > 0 and i < len(item) - 1 and 
                    item[i] % width != 0 and item[i] % width != width - 1 and 
                    int(item[i] / width) != 0 and int(item[i] / width) != height - 1 and 
                    item[i] == item[i - 1] - width - 1 and item[i] == item[i + 1] + width + 1):
                node_to_remove.append(item[i])

            # left down <-> right up
            elif (i > 0 and i < len(item) - 1 and 
                    item[i] % width != 0 and item[i] % width != width - 1 and 
                    int(item[i] / width) != 0 and int(item[i] / width) != height - 1 and 
                    item[i] == item[i - 1] + width - 1 and item[i] == item[i + 1] - width + 1):
                node_to_remove.append(item[i])
            elif (i > 0 and i < len(item) - 1 and 
                    item[i] % width != 0 and item[i] % width != width - 1 and 
                    int(item[i] / width) != 0 and int(item[i] / width) != height - 1 and 
                    item[i] == item[i - 1] - width + 1 and item[i] == item[i + 1] + width - 1):
                node_to_remove.append(item[i])

# construct new vectors with optimization
new_vectors = []
for opt_node_vector in opt_node_vectors:  # each color
    new_vector = []
    for node_list in opt_node_vector:  # each draw
        new_list = []
        for node in node_list:  # each node
            if node not in node_to_remove:
                new_list.append(node)
        new_vector.append(new_list)
    new_vectors.append(new_vector)

# print(new_vectors)
# new vectors contains the optimized vectors

#------------------------------------------------------------------------
# convert to angle

angle_vectors = []  # vectors holding angle for each color
for i in range(len(new_vectors)):
    angle_vector = []
    for a in new_vectors[i]:
        angle_list = []
        for element in a:

            x = int(element % width)
            y = int(element / width)

            try:
                pair = inv_kinematics(x, y, L1, L2, pixel_factor)
                angle_list.append(pair)
            except:
                print("out of boundary")
                a.remove(element)
        angle_vector.append(angle_list)
    angle_vectors.append(angle_vector)

#------------------------------------------------------------------------
# output up down angle signals

# for testing purpose, only draw black
black_index = 0
for i in range(len(picture_colors)):
    if picture_colors[i][0] == 0 and picture_colors[i][1] == 0 and picture_colors[i][2] == 0:
        black_index = i

if not os.path.exists('vector'):
    os.makedirs('vector')

for i in range(len(picture_colors)):
    # if picture_colors[i] == (252, 252, 252):
    #     continue

    file_name = "vector/vector" + str(i) + ".txt"
    print(str(picture_colors[i]) + ": " + file_name)

    vector_file = open(file_name, "w")

    vector_file.write("up\n")
    # change i here to black_index to test specific color
    for vector_item in angle_vectors[i]:
        # each list
        record = 0
        for item in vector_item:
            # each pair
            if record == 1:
                vector_file.write("down\n")
            first_step = int(item[0] * (200 * 16 * 10) / 360)
            second_step = int(item[1] * (200 * 16 * 10) / 360)
            vector_file.write("first: " + str(first_step) + "\n")
            vector_file.write("second: " + str(second_step) + "\n")
            record += 1
        if len(vector_item) == 1:
            vector_file.write("down\n")
        vector_file.write("up\n")


#------------------------------------------------------------------------
# output all pictures for animation

if animation == "true":

    im = Image.new("RGB", (width, height), "white")
    index = 0

    if not os.path.exists('output'):
        os.makedirs('output')

    for i in range(len(picture_colors)):
        for list in new_vectors[i]:
            for element in list:
                x = element % width
                y = int(element / width)
                im.putpixel(
                    (x, y), (picture_colors[i][0], picture_colors[i][1], picture_colors[i][2]))
                path = 'output/out_' + str(index) + '.png'
                im.save(path)
                index += 1
