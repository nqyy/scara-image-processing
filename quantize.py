#!/usr/bin/env python3
import sys
import PIL
from PIL import Image
import numpy


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


# main
# expected to use command: python3 quantize image.jpg color1 color2 color3
# white is used as the default 4th color
# last argument is the optional image resolution factor
# this function will output out_quantize.bmp
img = Image.open(sys.argv[1])

# all the colors we have right now
allcolors = {
    'red': (255, 0, 0),
    'orange': (255, 128, 0),
    'yellow': (255, 255, 0),
    'green': (0, 255, 0),
    'blue': (0, 0, 255),
    'purple': (128, 0, 128),
    'black': (0, 0, 0),
    'white': (255, 255, 255),
}
ourcolors = [allcolors[sys.argv[2]], allcolors[sys.argv[3]],
             allcolors[sys.argv[4]], (255, 255, 255)]
palettedata = []

for i in range(0, 4):
    for j in range(0, 3):
        palettedata.append(ourcolors[i][j])

palimage = Image.new('P', (16, 16))
palimage.putpalette(palettedata * 64)

finalimage = quantize(img, palimage, dither=False)

#resize
if sys.argv[5]:
    resize = float(sys.argv[5])
    nx, ny = finalimage.size
    finalimage = finalimage.resize((int(nx * resize), int(ny * resize)), Image.BICUBIC)

finalimage.show()

finalimage.save('out_quantize.bmp')
