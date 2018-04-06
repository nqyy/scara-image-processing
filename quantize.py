#!/usr/bin/env python3
import sys
import PIL
from PIL import Image
import numpy as np
import scipy as sp
import scipy.ndimage


def quantize(silf, palette, dither=False):
    """Convert an RGB or L mode image to use a given P image's palette."""

    silf.load()

    # use palette from reference image
    palette.load()
    if palette.mode != "P":
        raise ValueError("bad mode for palette image")
    if silf.mode != "RGB" and silf.mode != "L":
        raise ValueError(
            "only RGB or L mode images can be quantized to a palette"
        )
    im = silf.im.convert("P", 1 if dither else 0, palette.im)

    try:
        return silf._new(im)
    except AttributeError:
        return silf._makeself(im)


def fill_holes(finalimage):
    """ fill small holes of the image to make it smooth. it returns a filled a img"""

    im = finalimage.convert("RGB")
    width, height = im.size

    matrix1 = []
    matrix2 = []
    matrix3 = []

    for j in range(height):
        matrix1.append([])
        matrix2.append([])
        matrix3.append([])
        for i in range(width):
            matrix1[j].append(0)
            matrix2[j].append(0)
            matrix3[j].append(0)

    # fill in matrix with 0 and 1
    for y in range(height):
        for x in range(width):
            r, g, b = im.getpixel((x, y))
            # r,g,b = 0, 0, 0
            if r == ourcolors[0][0] and g == ourcolors[0][1] and b == ourcolors[0][2]:
                matrix1[y][x] = 1
            else:
                matrix1[y][x] = 0

    for y in range(height):
        for x in range(width):
            r, g, b = im.getpixel((x, y))
            # r,g,b = 0, 0, 0
            if r == ourcolors[1][0] and g == ourcolors[1][1] and b == ourcolors[1][2]:
                matrix2[y][x] = 1
            else:
                matrix2[y][x] = 0

    for y in range(height):
        for x in range(width):
            r, g, b = im.getpixel((x, y))
            # r,g,b = 0, 0, 0
            if r == ourcolors[2][0] and g == ourcolors[2][1] and b == ourcolors[2][2]:
                matrix3[y][x] = 1
            else:
                matrix3[y][x] = 0

    data1 = scipy.ndimage.morphology.binary_fill_holes(matrix1)
    data2 = scipy.ndimage.morphology.binary_fill_holes(matrix2)
    data3 = scipy.ndimage.morphology.binary_fill_holes(matrix3)

    im = Image.new("RGB", (width, height))

    for y in range(height):
        for x in range(width):
            if data1[y][x] == 1:
                im.putpixel(
                    (x, y), (ourcolors[0][0], ourcolors[0][1], ourcolors[0][2]))
                continue
            if data2[y][x] == 1:
                im.putpixel(
                    (x, y), (ourcolors[1][0], ourcolors[1][1], ourcolors[1][2]))
                continue
            if data3[y][x] == 1:
                im.putpixel(
                    (x, y), (ourcolors[2][0], ourcolors[2][1], ourcolors[2][2]))
                continue
            im.putpixel((x, y), (255, 255, 255))

    return im


# main
# expected to use command: python quantize.py
# please change quantize.config for certain behavior
# this function will output out_quantize.bmp

# get configuration from config file
try:
    s = open("quantize.config","r")
except:
    sys.exit("File 'quantize.config' is missing")

settings = s.readlines()
i = 0
for line in settings:
    settings[i] = line[line.index(":") + 2: -1]
    i+=1

image_name = settings[0]
colors = settings[1]
resolution_factor = float(settings[2])
fillholes = settings[3]
colorslist = []
colorslist = colors.split(" ")

#--------------------starts the program-----------------------

img = Image.open(image_name)

# all the colors we have right now
colorpool = {
    'red': (255, 0, 0),
    'orange': (255, 127, 0),
    'yellow': (255, 255, 0),
    'green': (0, 255, 0),
    'blue': (0, 0, 255),
    'purple': (127, 0, 127),
    'black': (0, 0, 0),
    'white': (255, 255, 255),
    'indigo': (75, 0, 130),
    # more colors can be added to our pool
}

ourcolors = [(255,255,255)]
for i in range(len(colorslist)):
    ourcolors.append(colorpool[colorslist[i]])

# print(ourcolors)
palettedata = []

for i in range(len(ourcolors)):
    for j in range(0, 3):
        palettedata.append(ourcolors[i][j])

palimage = Image.new('P', (16, 16))
palimage.putpalette(palettedata * int(256 / len(ourcolors)))

finalimage = quantize(img, palimage, dither=False)

# resize the image to specific resolution
resize = float(resolution_factor)
nx, ny = finalimage.size
finalimage = finalimage.resize(
    (int(nx * resize), int(ny * resize)), Image.BICUBIC)

# call fill holes
if fillholes == "true":
    im = fill_holes(finalimage)
else:
    im = finalimage

im.show()
im.save('out_quantize.bmp')

