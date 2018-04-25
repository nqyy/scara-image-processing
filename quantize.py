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

    matrixes = []
    for i in range (len(ourcolors)):
        matrixes.append([])

    for mat in matrixes:
        for j in range(height):
            mat.append([])
            for i in range(width):
                mat[j].append(0)

    data = []
    for i in range (len(ourcolors)):
        for y in range(height):
            for x in range(width):
                r, g, b = im.getpixel((x, y))
                if r == ourcolors[i][0] and g == ourcolors[i][1] and b == ourcolors[i][2]:
                    matrixes[i][y][x] = 1
                else:
                    matrixes[i][y][x] = 0
        data.append(scipy.ndimage.morphology.binary_fill_holes(matrixes[i]))

    im = Image.new("RGB", (width, height))

    for i in range (len(data)):
        for y in range(height):
            for x in range(width):
                if data[i][y][x] == 1:
                    im.putpixel((x, y), (ourcolors[i][0], ourcolors[i][1], ourcolors[i][2]))

    return im


# main
# expected to use command: python quantize.py
# please change quantize.config for certain behavior
# this function will output out_quantize.bmp

# get configuration from config file
try:
    s = open("configuration.config","r")
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
img = img.convert("RGB")

# all the colors we have right now
colorpool = {
    'red': (255, 0, 0),
    'orange': (255, 127, 0),
    'yellow': (255, 255, 0),
    'green': (0, 255, 0),
    'blue': (0, 0, 255),
    'purple': (127, 0, 127),
    'black': (0, 0, 0),
    # 'white': (255, 255, 255),
    'indigo': (75, 0, 130),
    'aqua' : (0, 255, 255)
    # more colors can be added to our pool
}

ourcolors = [(252,252,252)] # white
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
    print("holes filled")
else:
    im = finalimage

im.show()
im.save('out_quantize.bmp')

